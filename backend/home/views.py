import django.middleware.csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponsePermanentRedirect


# Create your views here.

def user_login(request):
    """
    View function for user login.
    For GET method view returns csrf token for login.
    For POST method view checks if user with given credentials exists and if exist redirects to contacts page.
    """
    if request.method == "GET":
        csrf = django.middleware.csrf.get_token(request)
        return JsonResponse({"csrf": csrf})
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponsePermanentRedirect("/contacts/")
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required(login_url='/login', redirect_field_name=None)
def user_logout(request):
    logout(request)
    response = HttpResponsePermanentRedirect('/login')
    response.set_cookie("sessionid", "", 0, "1970-01-01T00:00:00.000Z", "/")
    response.set_cookie("logged_in", "", 0, "1970-01-01T00:00:00.000Z", "/")
    response.set_cookie("csrftoken", "", 0, "1970-01-01T00:00:00.000Z", "/")
    return response
