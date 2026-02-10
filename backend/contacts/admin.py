from django.contrib import admin
from contacts.models import Contact, ContactStatusChoices, CityLocationWeather

admin.site.register(Contact)
admin.site.register(ContactStatusChoices)


class CityLocationWeatherAdmin(admin.ModelAdmin):
    """
        Custom Admin view for CityLocationWeather class
    """
    fieldsets = [
        (
            None,
            {
                'fields': ['name']
            }
        ),
        (
            "Advanced options",
            {
                "classes": ['collapse'],
                "fields": ["latitude", "longitude", "temperature", "humidity", "wind_speed"]
            }
        )
    ]


admin.site.register(CityLocationWeather, CityLocationWeatherAdmin)
