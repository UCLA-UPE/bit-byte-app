from django.shortcuts import render
from django.http import HttpResponse
from internal.models import *
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'internal/index.html', context)

def register(request):
    return render(request, 'internal/register.html')

def register_submit(request):
    try:
        # transform
        role = None
        if request.POST['role'] == "Bit": role = "b"
        elif request.POST['role'] == "Byte": role = "B"

        # validate
        assert role is not None
        assert len(request.POST['username']) >= 3
        assert len(request.POST['password']) >= 3
        assert len(request.POST['first_name']) >= 1
        assert len(request.POST['last_name']) >= 1

        # create user and profile
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        profile = Profile(user=user, role=role)

    except:
        # generic error
        return render(request, 'internal/registration.html', {
            'error_message': "Something went bad. Try again, but do it better.",
        })

    else:
        user.save()
        profile.save()
        return HttpResponse("Success.")

def edit(request):
    return HttpResponse("Hello, world.")
