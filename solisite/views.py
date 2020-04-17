from django.shortcuts import render, redirect
from accounts.models import Organiser

def landingpage_view(request):
    return render(request, 'solisite/landingpage.html')

def about_view(request):
    return render(request, 'solisite/about.html')

def imprint_view(request):
    return render(request, 'solisite/imprint.html')

def privacy_policy_view(request):
    return render(request, 'solisite/privacy_policy.html')

def blog_view(request):
    return render(request, 'solisite/blog.html')

def faq_view(request):
    return render(request, 'solisite/faq.html')

def agb_view(request):
    return render(request, 'solisite/agb.html')

def contact_view(request):
    return render(request, 'solisite/contact.html')
