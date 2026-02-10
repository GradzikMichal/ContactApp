from django.urls import path
from . import views

urlpatterns = [
    path("contacts/", views.contacts, name="contacts"),
    path("contacts/<int:contact_id>/", views.edit_delete_contact, name="contact"),
    path("contacts/upload/", views.upload_file, name="upload_file"),
]
