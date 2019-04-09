from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from internal.models import *

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
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login/', request.path))

    teams_raw = Team.objects.all()
    teams = []
    for team_raw in teams_raw:
        team = {'name': team_raw.name, 'points': team_raw.points}
        members = Profile.objects.filter(team=team_raw)
        try:
            team['byte'] = members.get(role='B')
        except Profile.DoesNotExist:
            team['byte'] = None
        team['bits'] = members.filter(role='b')
        teams.append(team)
    context = {'teams': teams}
    print(teams)
    return render(request, 'internal/teams.html', context)

def events_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login/', request.path))

    # either admin, byte, or bit
    p = Profile.objects.get(user=request.user)
    if request.user.is_staff: # Admin can edit all
        profiles = Profile.objects.all()
        editable = True

    elif p.role == "B": # Byte can view team
        profiles = Profile.objects.filter(team=p.team)
        editable = False

    elif p.role == "b": # Bit can view self
        profiles = [p]
        editable = False

    events = Event.objects.all()
    checkoffs = EventCheckoff.objects.all()
    checkoff_array = []
    for p in profiles:
        checks = []
        for e in events:
            check = checkoffs.filter(person=p, event=e).exists()
            checks.append({'check': check, 'event': e.id})
        checkoff_array.append({'profile': p, 'checks': checks})
    context = {'events': events, 'array': checkoff_array, 'editable': editable}

    return render(request, 'internal/events.html', context)

def events_submit_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login/', request.path))    # print(request.POST)

    if not request.user.is_staff:
        return HttpResponseForbidden('<h1>Forbidden: User is not allowed to edit event checkoffs.</h1>')

    for profile in Profile.objects.all():
        for event in Event.objects.all():
            # did_event = request.POST.get('did_event_%s_%s' % (str(profile.id), str(event.id)), "False") == "True"
            did_event = request.POST.get('cb_%s_%s' % (str(profile.id), str(event.id)))
            checkoff = EventCheckoff.objects.filter(person=profile.id, event=event.id)
            # print('cb_%s_%s %s' % (str(profile.id), str(event.id), str(did_event)))
            if did_event == "True" and not checkoff.exists():
                print("person %s event %s IS now checked, creating..." % (profile.user.first_name, event.name))
                checkoff = EventCheckoff(person=profile, event=event)
                checkoff.save()
            elif did_event == "False" and checkoff.exists():
                print("person %s event %s is now NOT checked, deleting..." % (profile.user.first_name, event.name))
                checkoff.get().delete()
                
    messages.add_message(request, messages.SUCCESS, "Event checkoffs successfully updated.")
    return redirect('/events/')

def edit(request):
    return HttpResponse("Hello, world.")
