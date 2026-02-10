from django.urls import path
from . import views

urlpatterns = [
    path("login", views.user_login, name="User login"),
    path("logout", views.user_logout, name="User logout"),
]