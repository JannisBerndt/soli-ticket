# Create your views here.
from django.shortcuts import render
from django.template import Context, loader
from register.models import User

def dashboard(request):
    users = User.objects.all()
    return render(request, "solisite/dashboard.html", {'users': users})
