from django.shortcuts import render, get_object_or_404
from django.contrib.auth import models
from .models import Organiser

def profile(request, pk):
    organiser = Organiser.objects.get(username=pk)
    context = {'organiser': organiser}
    return render(request, 'accounts/profile.html', context)
