from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import UserAddress, Organiser
from .forms import UserAddressForm, OrganiserForm, Register1, Register2, Register3
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from solisite.settings import DEBUG
import string
import random
from urllib.parse import urlencode


def login_page(request):
    if request.user.is_authenticated:
        username = request.user
        return redirect('events:event_organiser_list', Organiser.objects.get(username=username).organisation_name)
    else:
        if request.method == 'POST':
            
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                organiser = Organiser.objects.get(email=username)
                username = organiser.username
            except:
                pass
            try:
                organiser = Organiser.objects.get(organisation_name=username)
                username = organiser.username
            except:
                pass

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                o_organiser = Organiser.objects.get(username = user.username)
                if o_organiser is not None:
                    if o_organiser.isActivated == False:
                        params = urlencode({'code': o_organiser.confirmationCode})
                        url = "{}?{}".format(reverse('accounts:verify_email'), params)
                        return redirect(url)
                    else: 
                        login(request, user)
                        return redirect('events:event_organiser_list', Organiser.objects.get(username=username).organisation_name)
            else:
                messages.info(request, 'Username or Password is incorrect')
        try:
            organiser_user = Organiser.objects.get(username = request.user.username)
        except:
            organiser_user = None
        context = {
			'authenticated': request.user.is_authenticated,
			'organiser_user': organiser_user,
		}
        return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('accounts:login')

def verify_email_view(request):
    code = request.GET["code"]
    organiser = get_object_or_404(Organiser, confirmationCode=code)
    if request.method == 'POST':
        buildAndSendEmail(organiser)
    context = {
		'organiser_user': None,
        'code': code,
	}
    return render(request, 'register/check_your_emails.html', context)

def error(request):
    print("Error at registration")
    return render(request, 'register/error.html')

def organiser_list_view(request):
    organisers = Organiser.objects.filter(is_active=True)
    try:
        organiser_user = Organiser.objects.get(username = request.user.username)
    except:
        organiser_user = None
    addresses = UserAddress.objects.filter(organiser_address__is_active = True).distinct()
    print(addresses)
    cities = addresses.values('ort').order_by('ort')
    context = {
        'organisers': organisers,
        'organiser_user': organiser_user,
        'cities': cities,
    }
    return render(request, 'accounts/organiser_list.html', context)

@login_required(login_url='accounts:login')
def profile_update_view(request):
	user = request.user
	organiser = Organiser.objects.get(username=user.username)
	address = organiser.user_address
	if request.method == 'POST':
		organiser_form = OrganiserForm(request.POST, instance = organiser)
		address_form = UserAddressForm(request.POST, instance = address)
		if organiser_form.is_valid() and address_form.is_valid():
			organiser_form.save()
			address.save()
			return redirect('events:event_organiser_list', organiser=organiser)
	else:
		organiser_form = OrganiserForm(instance = organiser)
		address_form = UserAddressForm(instance = address)

	context = {
		'organiser_form': organiser_form,
		'address_form': address_form,
		'organiser_user': organiser,
	}
	return render(request, 'accounts/profile_update.html', context)

@login_required(login_url='accounts:login')
def profile_delete_view(request):
    user = request.user
    organiser = get_object_or_404(Organiser, username=user.username)
    if request.method == 'POST':
        logout(request)
        organiser.is_active = False
        organiser.save()
        return redirect('home')
    context = {
        'organiser_user': organiser,
    }
    return render(request, 'accounts/profile_delete.html', context)

class accounts(View):
    template_name = ['register/register_start.html',
                     'register/register_start2.html',
                     'register/register_start3.html',
					 'register/check_your_emails.html',
                     'register/register_finished.html']
    tags = ["email","pw","vname","nname","oname","art","strasse","username",
            "hnummer","plz","ort","telnr","kontoinhaber","iban","bic","kontourl", "description"]


    def get(self, request, *args, **kwargs):

        registerform = Register1()
        context = {
            'register1' : registerform,
        }
        return render(request, self.template_name[0], context)



    def post(self, request, *args, **kwargs):

        
        req = request.POST

        # Wir waren auf page 1:
        if "pw1" in req:
            form = Register1(request.POST)

            if form.is_valid() and form.cleaned_data['pw1'] == form.cleaned_data['pw2']:
                valid = True
                if Organiser.objects.filter(email = req.get('email')).exists():
                    valid = False
                    form.add_error('email', 'Diese Email wird bereits verwendet.')
                if Organiser.objects.filter(username = req.get('user')).exists():
                    valid = False
                    form.add_error('user', 'Der Username wird bereits verwendet.')
                if valid:
                    request.session["email"] = form.cleaned_data["email"]
                    request.session["pw"] = form.cleaned_data["pw1"]
                    request.session["username"] = form.cleaned_data["user"]
                    # "jump" to next page
                    form = Register2()
                    context = {
                        'register2' : form,
                    } 
                    return render(request, self.template_name[1], context)
                
            if form.cleaned_data['pw1'] != form.cleaned_data['pw2']:
                form.add_error('pw1', 'Die Passwörter stimmen nicht überein')
            context = {
                'register1' : form,
            }
            return render(request, self.template_name[0], context)

        # Wir waren auf page 2:
        elif "nname" in req:

            form = Register2(request.POST)
            if form.is_valid():
                valid = True
                if Organiser.objects.filter(organisation_name = req.get('oname')).exists():
                    valid = False
                    form.add_error('oname', 'Diese Organisation ist bereits registriert.')
                if valid:
                    for tag in ["vname","nname","oname","art","strasse",
                         "hnummer","plz","ort","telnr", "description"]:
                        request.session[tag] = form.cleaned_data[tag]
                    form = Register3()
                    context = {
                        'register3' : form,
                    }
                    return render(request, self.template_name[2], context)
            context = {
                'register2' : form,
            }
            return render(request, self.template_name[1], context)


            

        # Wir waren auf page 3:
        elif "paypal_email" in req:

            form = Register3(request.POST)
            if not form.is_valid():
                context = {
                    'register3' : form,
                }
                return render(request, self.template_name[2], context)
            

            for tag in ["paypal_email"]:
                request.session[tag] = form.cleaned_data[tag]


            #To Do: Implementierung der Datenbank
            objetct_useraddress = UserAddress(strasse = request.session["strasse"],
                                  hnummer = request.session["hnummer"],
                                  plz= request.session["plz"],
                                  ort = request.session["ort"].capitalize(),)
            objetct_useraddress.save()
            organiser = Organiser(user_address = objetct_useraddress,
                                  username = request.session["username"],
                                  organisation_name = request.session["oname"],
                                  organisation_type = request.session["art"],
                                  contact_first_name = request.session["vname"],
                                  contact_last_name = request.session["nname"],
                                  contact_phone = request.session["telnr"],
                                  email =request.session["email"],
								  description = request.session["description"],
                                  paypal_email = request.session["paypal_email"],
                                  isActivated = False)
            
            organiser.set_password(request.session["pw"])
            organiser.confirmationCode = confirmationCode_generator()
            organiser.save()

            organiser_user = Organiser.objects.get(username=request.session["username"])
            
            buildAndSendEmail(organiser_user)
        
            
            # Löschen der Sessions IDs:
            for tag in self.tags:
                try:
                    del request.session[tag]
                except KeyError:
                    pass
            
            params = urlencode({'code': organiser_user.confirmationCode})
            url = "{}?{}".format(reverse('accounts:verify_email'), params)
            return redirect(url)

        #To DO:
        # Umleitung auf Fehlerseite "Bitte Kontaktieren Sie uns"
        else:
            for tag in self.tags:
                del request.session[tag]
            response = redirect('error/')
            return response

def confirm(request):
    confirmation_Code = request.GET['confirmationCode']
    myid = request.GET['id']
    
    # In der URL ist die User-ID eingebaut. Theoretisch sollte man also immer User aus der DB kriegen zu dem die ID gehört
    organiser_user = Organiser.objects.get(id = myid)
    
    if organiser_user is None:
        return error
    # Check ob der in der URL vorhandene confirmationCode mit dem in der Datenbank übereinstimmt.
    if(confirmation_Code != organiser_user.confirmationCode):
        return error

    organiser_user.isActivated = True
    organiser_user.save()
    login(request, organiser_user)
    context = {
		'organiser_user': organiser_user,
    }
    return render(request, 'register/register_finished.html', context)
  
def buildAndSendEmail(o_organiser):
    email = o_organiser.email
    id = o_organiser.id
    o_code = o_organiser.confirmationCode
    
    if DEBUG:
        confirmLink = 'http://127.0.0.1:8000/accounts/confirm/?confirmationCode={organiser_code}&id={myid}'.format(organiser_code = o_code, myid = id)
    else:
        confirmLink = '{host}accounts/confirm/?confirmationCode={organiser_code}&id={myid}'.format(host = settings.HOST_URL_BASE, organiser_code = o_code, myid = id)


    subject = 'Bestätigung für die Registrierung auf Soli-Ticket'
    content =   'Vielen Dank für die Registrierung auf soli-ticket.de \n'\
                'Bitte klicken Sie auf den folgenden Link, um Ihren Account freizuschalten \n'\
                '{confirmLink} \n\n'\
                'Mit freundlichen Grüßen,\n\n'\
                'Ihr Soli-Ticket-Team'.format(confirmLink = confirmLink)

    if DEBUG:
        # Hier eure email eintragen, wenn ihr was testen wollt. 
        send_mail(subject, content, settings.EMAIL_HOST_USER, ['roessler.paul@web.de', 'kolzmertz@gmail.com', o_organiser.email])
    else:
        send_mail(subject, content, settings.EMAIL_HOST_USER, [o_organiser.email])

def confirmationCode_generator(size = 40, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

