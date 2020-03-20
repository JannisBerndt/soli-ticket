from django.shortcuts import render
from .models import Organiser
from register.forms import RegisterForm

def profile(request, pk):
    organiser = Organiser.objects.get(id=pk)

    context = {'organiser': organiser}
    return render(request, 'accounts/profile.html', context)

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'register/register_start.html', {'form': form})
    # for page 2:
    #return render(request, 'register/register_start2.html', {'form': form})
    # for page 3:
    #return render(request, 'register/register_start3.html', {'form': form})
