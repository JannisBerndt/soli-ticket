from django.shortcuts import render
from django.template import Context, loader
from accounts.models import Organiser

def dashboard(request):
    organisers = Organiser.objects.all()
    context = {'organisers': organisers}
    return render(request, "solisite/dashboard.html")
