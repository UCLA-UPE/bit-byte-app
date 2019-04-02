from django.shortcuts import render, redirect
from django.http import HttpResponse
from internal.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index_view(request):
    user = None

    if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
        user = request.user

    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'internal/index.html', context)

def register_view(request):
    return render(request, 'internal/register.html')

def register_submit_view(request):

    error_message = None
    site_settings = SiteSettings.load()

    # transform
    role = None
    if request.POST['role'] == "Bit": role = "b"
    elif request.POST['role'] == "Byte": role = "B"

    # validate
    if role == None: error_message = "role is invalid."
    if role == "b" and request.POST['invite'] != site_settings.bit_signup_pass:
        error_message = "the bit invite code is wrong."
    if role == "B" and request.POST['invite'] != site_settings.byte_signup_pass:
        error_message = "the byte invite code is wrong."
    if len(request.POST['username']) < 3: error_message = "username is too short."
    if len(request.POST['password']) < 3: error_message = "password is too short."
    if len(request.POST['first_name']) < 1: error_message = "first name is too short."
    if len(request.POST['last_name']) < 1: error_message = "last name is too short."
    if error_message != None:
        return render(request, 'internal/register.html', {'error_message': error_message})

    try:
        # create user and profile
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        profile = Profile(user=user, role=role)
    except:
        # generic error
        return render(request, 'internal/register.html', {
            'error_message': "Something went bad. Try again, but do it better.",
        })
    else:
        user.save()
        profile.save()
        login(request, user)
        return redirect('/profile/')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/profile/')
    return render(request, 'internal/login.html')

def login_submit_view(request):
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return redirect('/profile/')
    return render(request, 'internal/login.html', {
        'error_message': "Failed to authenticate.",
    })

def logout_view(request):
    logout(request)
    return redirect('/login/')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login/', request.path))

    context = {'profile': Profile.objects.get(user=request.user),
               'user': request.user}
    return render(request, 'internal/profile.html', context)

def teams_view(request):
    teams = Team.objects.all()
    choices = Choice.objects.filter(final=True)

    context = {'teams': teams,
               'choices': choices}

    return render(request, 'internal/teams.html', context)

def edit(request):
    return HttpResponse("Hello, world.")
