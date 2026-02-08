from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from .models import Contact

# Create your views here.
@login_required(login_url='/login', redirect_field_name=None)
def contacts(request):
    if request.method == 'GET':
        user_contacts = Contact.objects.filter(user_id=request.user).all()
        return JsonResponse(
            serialize(
                'json',
                user_contacts,
                fields=("name", "surname", "email", "phone", "city", "status", "add_date")
            ),
            safe=False
            )

@login_required(login_url='/login', redirect_field_name=None)
def new_contact(request):
    if request.method == 'GET':
        form = ContactForm()
        return HttpResponse(form)
    elif request.method == 'POST':
        form = ContactForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()

