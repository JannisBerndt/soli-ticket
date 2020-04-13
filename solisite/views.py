from django.shortcuts import render, redirect
from accounts.models import Organiser
from django.views.decorators.csrf import csrf_exempt
import stripe
def landingpage_view(request):
    return render(request, 'solisite/landingpage.html')

def about_view(request):
    return render(request, 'solisite/about.html')

@csrf_exempt
def oauth_view(request):
    state = request.GET.get('state')
    print(state)
    o_Organisation = Organiser.objects.get(paypal_email = 'berndtjannis@gmail.com')
    print(o_Organisation)
    #if (o_Organisation is not None):
    print('Hello')
    code = request.GET.get('code')
    response = stripe.OAuth.token(grant_type="authorization_code", code=code,)
    print(response)
    connected_account_id = response["stripe_user_id"]
    print(connected_account_id)
    o_Organisation.stripe_account_id = connected_account_id
    o_Organisation.save()
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
