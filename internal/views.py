from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from internal.models import *
from internal.forms import ProfileForm
import string
import random

# Create your views here.
def index_view(request):
    return redirect('/profile/')

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

def edit_profile_view(request):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % ('/login/', request.path))

	if request.method == "POST":
		form = ProfileForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('/profile/')
	else:
		form = ProfileForm(instance=request.user)

	return render(request, 'internal/editprofile.html', {'form': form})

def teams_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login/', request.path))

    teams_raw = Team.objects.all()
    teams = []
    for team_raw in teams_raw:
        team = {'name': team_raw.name, 'points': team_raw.points()}
        members = Profile.objects.filter(team=team_raw)
        byte = members.filter(role='B')
        if byte.exists():
            team['byte'] = byte.get()
        else:
            team['byte'] = None
        team['bits'] = members.filter(role='b')
        team['cur_user'] = members.filter(user=request.user).exists()
        teams.append(team)

    # sort in descending score
    teams_sorted = sorted(teams, key=lambda team: float(team['points']), reverse=True)

    team = request.user.profile.team
    team_name = None if team == None else team.name
    byte_invite_code = None
    if request.user.profile.role == 'B' and team != None:
        byte_invite_code = team.invite_code

    context = {'teams': teams_sorted, 'role': request.user.profile.role, 'team_name': team_name, 'byte_invite_code': byte_invite_code}
    return render(request, 'internal/teams.html', context)

def teams_create_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login/', request.path))
    elif request.user.profile.role != 'B':
        return HttpResponseForbidden('<h1>Forbidden: Only bytes are allowed to create a team.</h1>')
    elif request.user.profile.team != None:
        return HttpResponseForbidden('<h1>Forbidden: User already has a team. Please contact an administrator to modify existing team assignments.</h1>')

    name = request.POST.get('team_name')
    if name == None or len(name) < 3:
        return HttpResponse('<h1>Team name is too short.</h1>')

    invite_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    team = Team(name=name, invite_code=invite_code)
    team.save()

    request.user.profile.team = team
    request.user.profile.save()

    return redirect('/teams/')

def teams_join_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login/', request.path))
    elif request.user.profile.team != None:
        return HttpResponseForbidden('<h1>Forbidden: User already has a team. Please contact an administrator to modify existing team assignments.</h1>')

    invite_code = request.POST.get('invite_code')
    team = Team.objects.filter(invite_code=invite_code)

    if not team.exists():
        return HttpResponse('<h1>No team found.</h1>')
    elif len(team) > 1:
        return HttpResponse('<h1>Congratulate your byte on achieving a one-in-2176782336-chance key collision.</h1>')

    request.user.profile.team = team[0]
    request.user.profile.save()

    return redirect('/teams/')

def events_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login/', request.path))

    # either admin, byte, or bit
    p = Profile.objects.get(user=request.user)
    editable = False
    if request.user.is_staff: # Admin can edit all
        profiles = Profile.objects.filter(role__isnull=False)
        editable = True

    elif p.team == None or p.role == "b": # Teamless and bit can view self
        profiles = [p]

    elif p.role == "B": # Byte with team can view team
        profiles = Profile.objects.filter(role__isnull=False, team=p.team)

    events = Event.objects.all().order_by('id')
    checkoffs = EventCheckoff.objects.all()

    teams = {}
    for p in profiles:
        checks = []
        # all events for this person
        for e in events:
            count = checkoffs.filter(person=p, event=e).count()
            checks.append({'repeatable': e.repeatable, 'count': count, 'event': e.id})
        # insert this person into a team
        # assign id=0 for teamless people
        team_id = 0 if p.team == None else p.team.id
        # create dict entry if team does not exist
        if team_id not in teams:
            teams[team_id] = {'team_name': '(Teamless)' if team_id == 0 else p.team.name, 'members': []}
        # make sure bytes are first
        if p.role == 'B':
            teams[team_id]['members'] = [{'profile': p, 'checks': checks}] + teams[team_id]['members']
        else:
            teams[team_id]['members'].append({'profile': p, 'checks': checks})
    
    context = {'events': events, 'teams': teams, 'editable': editable}
    return render(request, 'internal/events.html', context)

def events_submit_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login/', request.path))    # print(request.POST)

    if not request.user.is_staff:
        return HttpResponseForbidden('<h1>Forbidden: User is not allowed to edit event checkoffs.</h1>')

    for profile in Profile.objects.all():
        for event in Event.objects.all():
            did_event_count = request.POST.get('cb_%s_%s' % (str(profile.id), str(event.id)))
            if did_event_count == None:
                continue
            did_event_count = int(did_event_count)
            checkoffs = EventCheckoff.objects.filter(person=profile.id, event=event.id)
            while checkoffs.count() < int(did_event_count): # create some checkoffs...
                co = EventCheckoff(person=profile, event=event)
                co.save()
            while checkoffs.count() > int(did_event_count): # delete some checkoffs...
                checkoffs[0].delete()

    messages.add_message(request, messages.SUCCESS, "Event checkoffs successfully updated.")
    return redirect('/events/')

def edit(request):
    return HttpResponse("Hello, world.")
