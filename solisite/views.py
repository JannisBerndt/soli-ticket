from django.shortcuts import render, redirect
from accounts.models import Organiser
import stripe
def landingpage_view(request):
    try:
        organiser_user = Organiser.objects.get(username = request.user.username)
    except:
        organiser_user = None
    print(organiser_user)
    context = {
        'authenticated': request.user.is_authenticated,
        'organiser_user': organiser_user,
    }
    return render(request, 'solisite/landingpage.html', context)

def about_view(request):
    try:
        organiser_user = Organiser.objects.get(username = request.user.username)
    except:
        organiser_user = None
    context = {
        'authenticated': request.user.is_authenticated,
        'organiser_user': organiser_user,
    }
    return render(request, 'solisite/about.html', context)

def oauth_view(request):
    state = request.GET.get('state')
    o_Organisation = Organiser.objects.get(id = state)
    
    if (o_Organisation is not None):
        code = request.GET.get('code')
        response = stripe.OAuth.token(grant_type="authorization_code", code=code,)
        connected_account_id = response["stripe_user_id"]
        o_Organisation.stripe_user_id = connected_account_id
        o_Organisation.save()
    
    return render(request, 'solisite/about.html')
            

def imprint_view(request):
    try:
        organiser_user = Organiser.objects.get(username = request.user.username)
    except:
        organiser_user = None
    context = {
        'authenticated': request.user.is_authenticated,
        'organiser_user': organiser_user,
    }
    return render(request, 'solisite/imprint.html', context)

def privacy_policy_view(request):
    try:
        organiser_user = Organiser.objects.get(username = request.user.username)
    except:
        organiser_user = None
    context = {
        'authenticated': request.user.is_authenticated,
        'organiser_user': organiser_user,
    }
    return render(request, 'solisite/privacy_policy.html', context)

def blog_view(request):
    try:
        organiser_user = Organiser.objects.get(username = request.user.username)
    except:
        organiser_user = None
    context = {
        'authenticated': request.user.is_authenticated,
        'organiser_user': organiser_user,
    }
    return render(request, 'solisite/blog.html', context)

def faq_view(request):
    try:
        organiser_user = Organiser.objects.get(username = request.user.username)
    except:
        organiser_user = None
    context = {
        'authenticated': request.user.is_authenticated,
        'organiser_user': organiser_user,
    }
    return render(request, 'solisite/faq.html', context)

def agb_view(request):
    try:
        organiser_user = Organiser.objects.get(username = request.user.username)
    except:
        organiser_user = None
    context = {
        'authenticated': request.user.is_authenticated,
        'organiser_user': organiser_user,
    }
    return render(request, 'solisite/agb.html', context)
