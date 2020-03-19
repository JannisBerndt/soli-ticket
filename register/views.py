from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm

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
