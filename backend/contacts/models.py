from typing import Any

from django.contrib.auth.models import User
from django.db import models
import requests
from requests.models import Response
import datetime as dt
from datetime import datetime, timedelta
from django.utils.http import urlencode
import openmeteo_requests
import requests_cache
from retry_requests import retry


# Create your models here.
class ContactStatusChoices(models.Model):
    """
    Contact status choices class which stores contact status like 'new', 'active', 'inactive'

    :param id: Contact status id, autoincrement
    :param name: Contact status name like 'new', 'active', 'inactive' etc.
    :return: Contact status choices object
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        """
            Name of an object on admin page
            :return: Name of the object as string
            :rtype: str
        """
        return self.name


class CityLocationWeather(models.Model):
    """
    City location and weather class which stores cities, its lat/lon and weather conditions

    :param name: City name
    :param latitude: City latitude
    :param longitude: City longitude
    :param temperature: City temperature
    :param humidity: City humidity
    :param wind_speed: City wind speed
    :return: City location object
    """
    name = models.CharField(max_length=100, primary_key=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, unique=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, unique=True, blank=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, unique=True, blank=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, unique=True, blank=True)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, unique=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Name of an object on admin page
        :return: Name of the object as string
        :rtype: str
        """
        return self.name

    def _get_coordinates(self) -> (float, float):
        query = {
            "q": self.name,
            "format": "json",
            "limit": 1
        }
        response: Response = requests.get(
            f"https://nominatim.openstreetmap.org/search?" + urlencode(query),
            headers={"User-Agent": "Recruitment-Task"},
        )
        response: dict[str, Any] = response.json()[0]
        return float(response["lat"]), float(response["lon"])

    def _get_weather(self) -> (float, float, float):
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d"),
        }
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        current = response.Current()
        return current.Variables(0).Value(), current.Variables(1).Value(), current.Variables(2).Value()

    def save(self, **kwargs):
        try:
            if self not in list(CityLocationWeather.objects.all()):
                self.latitude, self.longitude = self._get_coordinates()
                self.temperature, self.humidity, self.wind_speed = self._get_weather()
            else:
                print(datetime.now(dt.UTC) - self.last_updated > timedelta(hours=1))
                if datetime.now(dt.UTC) - self.last_updated > timedelta(hours=1):
                    self.temperature, self.humidity, self.wind_speed = self._get_weather()
            super().save(**kwargs)
        except Exception as e:
            print(e)
            return


class Contact(models.Model):
    """
    Contact class which stores contact information

    :param id: Contact id, autoincrement
    :param name: Contact name
    :param surname: Contact surname
    :param email: Contact email
    :param phone: Contact phone with country code prefix like +48
    :param city: Contact place of leaving
    :param status: Contact status
    :param add_date: Contact add date

    :return: Contact object
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    city = models.ForeignKey(CityLocationWeather, on_delete=models.PROTECT)
    status = models.ForeignKey(ContactStatusChoices, on_delete=models.PROTECT)
    add_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ManyToManyField(User)

    def __str__(self):
        """
            Whole name of a contact on admin page
            :return: Whole name of the object as string
            :rtype: str
        """
        return self.name + " " + self.surname
