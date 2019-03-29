from django.shortcuts import render
from django.http import HttpResponse
from internal.models import *
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'internal/index.html', context)

def registration(request):
    return render(request, 'internal/registration.html')

def register(request):
    # transformations
    if request.POST['role'] == "Bit": role = "b"
    elif request.POST['role'] == "Byte": role = "B"

    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']

    profile = Profile(user=user, role=role)

    user.save()
    profile.save()

    return HttpResponse("Success.")



def edit(request):
    return HttpResponse("Hello, world.")
