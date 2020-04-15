from django.shortcuts import render, redirect
from accounts.models import Organiser
from django.views.decorators.csrf import csrf_exempt
import braintree

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

@csrf_exempt
def oauth(request):
    gateway = braintree.BraintreeGateway(client_id="client_id$sandbox$p6fg6pm5znyzsrxt", client_secret="client_secret$sandbox$f9a511f49e52b32c50bbebbdc08a49b3")
    
    state = request.POST.get('state')
    code = request.POST.get('code')
    result = gateway.oauth.create_token_from_code({
    "code": code
    })

    access_token = result.credentials.access_token
    #expires_at = result.credentials.expires_at
    refresh_token = result.credentials.refresh_token

