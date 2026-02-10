import json

import requests
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Contact, CityLocationWeather, ContactStatusChoices
import polars as pl


def create_or_update_contact(data) -> None:
    """
    Create a contact if it doesn't already exist or update if it does.'
    :param request: Request object
    :type request: Request
    :return: None
    :rtype:
    """
    new_data = data["data"]
    if not CityLocationWeather.objects.filter(name=new_data["city"]).exists():
        CityLocationWeather.objects.create(
            name=new_data["city"],
        )

    if not Contact.objects.filter(phone=new_data["phone"]).exists() and not Contact.objects.filter(
            email=new_data["email"]).exists():
        new_contact = Contact.objects.create(
            name=new_data["name"],
            surname=new_data["surname"],
            phone=new_data["phone"],
            email=new_data["email"],
            city=CityLocationWeather.objects.get(name=new_data["city"]),
            status=ContactStatusChoices.objects.get(name=new_data["status"]),
        )
        new_contact.save()
        new_contact.user_id.add(data["id"])
    elif Contact.objects.filter(phone=new_data["phone"]).exists():
        Contact.objects.get(phone=new_data["phone"]).user_id.add(data["id"])
    elif Contact.objects.filter(email=new_data["email"]).exists():
        Contact.objects.get(email=new_data["email"]).user_id.add(data["id"])


def get_user_contacts(request) -> JsonResponse:
    """
    Get all contact objects for a user
    :param request: User request
    :type request: Request
    :return:
    :rtype:
    """
    user_contacts = Contact.objects.select_related("city").select_related("status").filter(
        user_id=request.user).all()
    contact_statuses = list(ContactStatusChoices.objects.all().values("name"))
    data = {
        "contacts": serialize(
            "json",
            user_contacts,
            fields=("name", "surname", "email", "phone", "city", "status", "add_date"),
            use_natural_foreign_keys=True,
            use_natural_primary_keys=True,
        ),
        "csrf": request.META["CSRF_COOKIE"],
        "contact_statuses": contact_statuses,
    }
    return JsonResponse(
        data,
        safe=False
    )


# Create your views here.
@login_required(login_url='/login', redirect_field_name=None)
def contacts(request) -> JsonResponse:
    """
        View function for contacts page. This view is responsible for rendering the contact page and for adding new contacts.
        :param request: Either GET or POST request
        :type request: Request
        :return: JsonResponse
        :rtype: json
    """
    if request.method == 'GET':
        """
        Get all user contacts. 
        :return: JsonResponse
        """
        return get_user_contacts(request)

    elif request.method == 'POST':
        """
        Create a new contact. If contact already exists, update it by adding user to `user_id` field.
        :return: JsonResponse
        """
        try:
            data = {
                "id": request.user.id,
                "data": json.loads(request.body),
            }
            create_or_update_contact(data)
            return JsonResponse(
                serialize(
                    "json",
                    Contact.objects.select_related("city").select_related("status").filter(user_id=request.user).all(),
                    fields=("name", "surname", "email", "phone", "city", "status", "add_date"),
                    use_natural_foreign_keys=True,
                    use_natural_primary_keys=True,
                ),
                safe=False
            )
        except Exception as error:
            print(error)
            return JsonResponse({"message": "Something went wrong with creating a contact."})
    else:
        return JsonResponse({"message": "Method not allowed"})


def update_contact(request, contact_id: int) -> str:
    """
        Update a contact by ID.
        :param request: PUT request
        :type request: Request
        :param contact_id: Contact ID to update
        :type contact_id: int
        :return: JsonResponse
        :rtype:
    """
    data = json.loads(request.body)
    contact = Contact.objects.filter(user_id=request.user).get(id=contact_id)
    if contact is not None:
        contact.update_contact(data)
        contact.save()
        return "Contact successfully updated"
    return "Contact either does not exist or is not yours"


def delete_contact(request, contact_id: int) -> str:
    """
        Delete a contact by ID or remove user from `user_id` field.
        :param request: DELETE request
        :type request: Request
        :param contact_id: Contact ID to update
        :type contact_id: int
        :return: JsonResponse
        :rtype:
    """
    contact = Contact.objects.filter(user_id=request.user).get(id=contact_id)
    if contact is not None:
        contact.user_id.remove(request.user.id)
        if contact.user_id.all().count() == 0:
            contact.delete()
        return "Contact successfully deleted"
    return "Contact either does not exist or is not yours"


@login_required(login_url='/login', redirect_field_name=None)
def edit_delete_contact(request, contact_id: int) -> JsonResponse:
    """
        View function for contacts page. This view is responsible for updating or deleting a contact.
        :param request: Either PUT or DELETE request
        :type request: Request
        :param contact_id: Contact ID
        :type contact_id: int
        :return: JsonResponse
        :rtype: json
    """
    if request.method == 'PUT':
        return JsonResponse(data={"message":update_contact(request, contact_id)})
    elif request.method == 'DELETE':
        return JsonResponse(data={"message": delete_contact(request, contact_id)})
    else:
        return JsonResponse({"message": "Method not allowed"})


@login_required(login_url='/login', redirect_field_name=None)
def upload_file(request) -> JsonResponse:
    """
        Function handling the upload of a file containing contact data.
        :param request:
        :type request:
        :return:
        :rtype:
    """
    if request.method == 'POST':
        csv = pl.read_csv(request.body)
        needed_columns = {"name", "surname", "phone", "email", "city", "status"}
        file_columns = set(csv.columns)
        if len(file_columns.intersection(needed_columns)) == len(needed_columns):
            for row in csv.to_dicts():
                data = {
                    "id": request.user.id,
                    "data": row,
                }
                create_or_update_contact(data)
                return get_user_contacts(request)
        else:
            print("Something went wrong")
            return JsonResponse({"message": "Some columns are missing"})
