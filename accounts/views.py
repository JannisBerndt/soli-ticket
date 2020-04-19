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
from .filters import OrganiserFilter
from django.db.models.query import QuerySet
from urllib.parse import urlencode
from events.models import Event
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def login_view(request):
    if request.user.is_authenticated:
        username = request.user
        return redirect('accounts:profile', Organiser.objects.get(username=username).organisation_name)
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
                        buildAndSendEmail(o_organiser)
                        request.session['username'] = username
                        return redirect('accounts:verify_email')
                    else:
                        login(request, user)
                        return redirect('accounts:profile', Organiser.objects.get(username=username).organisation_name)
            else:
                messages.info(request, 'Username or Password is incorrect')
        context = {
			'authenticated': request.user.is_authenticated,
		}
        return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def verify_email_view(request):
    assert(request.session.get('username')), "The username has to be in the session before this view is called!"
    organiser = get_object_or_404(Organiser, username=request.session.get('username'))
    if request.method == 'POST':
        buildAndSendEmail(organiser)
    context = {
        'organiser': organiser,
	}
    return render(request, 'register/check_your_emails.html', context)

def error_view(request):
    print("Error at registration")
    return render(request, 'register/error.html')


def organiser_list_view(request):
    organisers = Organiser.objects.filter(is_active=True)

    myFilter = OrganiserFilter(request.GET, queryset=organisers)
    organisers = myFilter.qs
    list_of_ids = []
    for organiser in organisers:
        list_of_ids.append(organiser.user_address.id)
    addresses = UserAddress.objects.filter(id__in=list_of_ids).distinct()
    cities = addresses.values('ort').order_by('ort')
    context = {
        'organisers': organisers,
        'cities': cities,
        'myFilter': myFilter,
    }
    return render(request, 'accounts/organiser_list.html', context)


def profile_view(request, organisation_name):
	organiser_object = get_object_or_404(Organiser, organisation_name = organisation_name)
	event_list = Event.objects.filter(creator = organiser_object)
	event_list = event_list.order_by('date')
	user = request.user
	logged_in = user.username == organiser_object.username
	context = {
		'organiser': organiser_object,
		'event_list': event_list,
	}

	if(logged_in):
		return render(request, "accounts/profile_organiser.html", context)
	else:
		return render(request, "accounts/profile_customer.html", context)


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
			return redirect('accounts:profile', organisation_name=organiser.organisation_name)
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
                if Organiser.objects.filter(organisation_name = req.get('oname')).exists() or req.get('oname') == "edit" or req.get('oname') == "delete":
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


            for tag in ["paypal_email", "acceptedTac"]:
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
                                  isActivated = False,
                                  acceptedTac = request.session["acceptedTac"],)

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
            
            request.session['username'] = organiser_user.username
            return redirect('accounts:verify_email')

        #To DO:
        # Umleitung auf Fehlerseite "Bitte Kontaktieren Sie uns"
        else:
            for tag in self.tags:
                del request.session[tag]
            response = redirect('error/')
            return response


def confirm_view(request):
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
    subject = '[Soli-Ticket] Registrierung abschließen'
    html_message = render_to_string('email/double_opt_in.html', {'organiser': o_organiser})
    plain_message = strip_tags(html_message)
    if settings.DEBUG:
        to = ['roessler.paul@web.de', 'kolzmertz@gmail.com', o_organiser.email]
    else:
        to = [o_organiser.email]
    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, to, html_message = html_message)

def confirmationCode_generator(size = 40, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
