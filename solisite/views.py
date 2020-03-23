from django.shortcuts import render, redirect

def landingpage_view(request):
    context = {

    }
    return render(request, 'solisite/landingpage.html', context)