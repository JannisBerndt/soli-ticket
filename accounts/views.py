from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserAddress, Organiser
from .forms import UserAddressForm, OrganiserForm, Register1, Register2, Register3
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from solisite.settings import DEBUG
import string
import random


def login_page(request):
    if request.user.is_authenticated:
        username = request.user
        return redirect('events:event_organiser_list', Organiser.objects.get(username=username).organisation_name)
    else:
        if request.method == 'POST':
            
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                o_organiser = Organiser.objects.get(username = user.username)
                if o_organiser is not None:
                    if o_organiser.isActivated == False:
                        return render(request, 'register/confirm_Email.html')
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




# @login_required(login_url='login')
# def profile(request):
#     if request.user.is_authenticated:
#         pk = request.user.username
#     try:
#         organiser = Organiser.objects.get(username=pk)
#     except:
#         return redirect('home')
#     context = {
# 		'organiser': organiser,
# 		'authenticated': request.user.is_authenticated,
# 	}
#     return render(request, 'accounts/profile.html', context)


def error(request):
    print("Error at registration")
    return render(request, 'register/error.html')

def organiser_list_view(request):
	organisers = Organiser.objects.all()
	try:
		organiser_user = Organiser.objects.get(username = request.user.username)
	except:
		organiser_user = None
	cities = UserAddress.objects.values('ort').distinct().order_by('ort')
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

class accounts(View):
    template_name = ['register/register_start.html',
                     'register/register_start2.html',
                     'register/register_start3.html',
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
                    request.session["email"] = req.get("email")
                    request.session["pw"] = req.get("pw1")
                    request.session["username"] = req.get("user")
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
                        request.session[tag] = req.get(tag)
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
                request.session[tag] = req.get(tag)


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

            return render(request, self.template_name[3])

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
    return render(request, 'register/register_finished.html')
  
def buildAndSendEmail(o_organiser):
    email = o_organiser.email
    id = o_organiser.id
    o_code = o_organiser.confirmationCode
    
    if DEBUG:
        confirmLink = 'http://127.0.0.1:8000/accounts/confirm/?confirmationCode={organiser_code}&id={myid}'.format(organiser_code = o_code, myid = id)
    else:
        confirmLink = 'https://www.soli-ticket.de/accounts/confirm/?confirmationCode={organiser_code}&id={myid}'.format(organiser_code = o_code, myid = id)


    subject = 'Bestätigung für die Registrierung auf Soli-Ticket'
    content =   'Vielen Dank für die Registrierung auf soli-ticket.de \n'\
                'Bitte klicken Sie auf den folgenden Link, um Ihren Account freizuschalten \n'\
                '{confirmLink} \n\n'\
                'Mit freundlichen Grüßen,\n\n'\
                'Ihr Soli-Ticket-Team'.format(confirmLink = confirmLink)

    if DEBUG:
        # Hier eure email eintragen, wenn ihr was testen wollt. 
        send_mail(subject, content, settings.EMAIL_HOST_USER, ['roessler.paul@web.de'])
    else:
        send_mail(subject, content, settings.EMAIL_HOST_USER, [o_organiser.email])

def confirmationCode_generator(size = 40, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

