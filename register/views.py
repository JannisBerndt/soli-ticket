from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, DetailForm

def register_start(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detail')

    context = {'form': form}
    return render(request, 'register/register_start.html', context)

def register_detail(request):
    form = DetailForm()
    if request.method == "POST":
        form = DetailForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'register/register_detail.html', context)
