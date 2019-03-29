from django.shortcuts import render
from django.http import HttpResponse
from internal.models import *

# Create your views here.
def index(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, 'internal/index.html', context)

def register(request):
    # return HttpResponse("Hello, world. You're at the sdsdd index.")
    # return render(request, 'polls/index.html', context)
    return render(request, 'bit-byte-app/register.html')
