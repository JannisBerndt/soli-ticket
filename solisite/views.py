from django.shortcuts import render, redirect
from accounts.models import Organiser

def landingpage_view(request):
    return render(request, 'solisite/landingpage.html', context)

def about_view(request):
    return render(request, 'solisite/about.html', context)

def imprint_view(request):
    return render(request, 'solisite/imprint.html', context)

def privacy_policy_view(request):
    return render(request, 'solisite/privacy_policy.html', context)

def blog_view(request):
    return render(request, 'solisite/blog.html', context)

def faq_view(request):
    return render(request, 'solisite/faq.html', context)

def agb_view(request):
    return render(request, 'solisite/agb.html', context)
