import django.middleware.csrf
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponsePermanentRedirect


# Create your views here.

def user_login(request):
    """
    View function for user login.
    For GET method view returns csrf token for login.
    For POST method view checks if user with given credentials exists and if exist redirects to contacts page.
    """
    if request.method == "GET":
        return JsonResponse({"csrf": django.middleware.csrf.get_token(request)})
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponsePermanentRedirect("/contacts/")
        else:
            return JsonResponse({"error": "Invalid credentials"})
    else:
        return JsonResponse({"error": "Method not allowed"})
