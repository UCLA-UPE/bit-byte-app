from django.shortcuts import render, redirect

# Create your views here.
def index_view(request):
    # return
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % ('/login/', request.path))
    return render(request, 'wiki/base.html')
