from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from .forms import RegisterForm

def user_list(request):
    users = User.objects.all()
    return render(request, 'register/user_list.html', {'users': users})

def register_start(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return HttpResponse("Success")
    else:
        form = RegisterForm()
    return render(request, 'register/register_start.html', {'form': form})
