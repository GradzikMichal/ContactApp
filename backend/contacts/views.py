import json
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Contact, CityLocationWeather, ContactStatusChoices


def create_or_update_contact(request):
    """
    Create a contact if it doesn't already exist or update if it does.'
    :param request: Request object
    :type request: Request
    :return: None
    :rtype:
    """
    new_data = json.loads(request.body)
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
        new_contact.user_id.add(request.user.id)
    elif Contact.objects.filter(phone=new_data["phone"]).exists():
        Contact.objects.get(phone=new_data["phone"]).user_id.add(request.user.id)
    elif Contact.objects.filter(email=new_data["email"]).exists():
        Contact.objects.get(email=new_data["email"]).user_id.add(request.user.id)


# Create your views here.
@login_required(login_url='/login', redirect_field_name=None)
def contacts(request):
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

    elif request.method == 'POST':
        """
        Create a new contact. If contact already exists, update it by adding user to `user_id` field.
        :return: JsonResponse
        """
        try:
            create_or_update_contact(request)
            return JsonResponse(
                serialize(
                    "json",
                    Contact.objects.select_related("city").select_related("status").filter(user_id=request.user).all(),
                    fields=("name", "surname", "email", "phone", "city", "status", "add_date"),
                    use_natural_foreign_keys=True,
                    use_natural_primary_keys=True,
                ),
                safe=False,
                status=201
            )
        except Exception as error:
            print(error)
            return JsonResponse({"message": "Something went wrong with creating a contact."}, status=500)

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


def update_contact(request, contact_id: int):
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
        return JsonResponse({"message": "Contact successfully updated"}, status=201)
    return JsonResponse({"message": "Contact either does not exist or is not yours"}, status=404)


def delete_contact(request, contact_id: int):
    contact = Contact.objects.filter(user_id=request.user).get(id=contact_id)
    if contact is not None:
        contact.user_id.remove(request.user.id)
        if contact.user_id.all().count() == 0:
            contact.delete()
        return JsonResponse({"message": "Contact successfully deleted"}, status=204)
    return JsonResponse({"message": "Contact either does not exist or is not yours"}, status=404)


@login_required(login_url='/login', redirect_field_name=None)
def edit_delete_contact(request, contact_id: int):
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
        return update_contact(request, contact_id)
    elif request.method == 'DELETE':
        return delete_contact(request, contact_id)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)
