from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserAddress, Organiser


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

class accounts(View):
    template_name = ['register/register_start.html',
                     'register/register_start2.html',
                     'register/register_start3.html',
                     'register/register_finished.html']
    context = {"error1" : "",
               "error2" : "",
               "error3" : "",
               "error4" : "",
               "error5" : "",
               "error6" : "",
			   'authenticated': False,
			   'organiser_user': None,}
    tags = ["email","pw","vname","nname","oname","art","strasse","username",
            "hnummer","plz","ort","telnr","kontoinhaber","iban","bic","kontourl"]


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name[0])



    def post(self, request, *args, **kwargs):

        # Errors "clearen"
        for error in self.context.keys():
            self.context[error] = ""

        req = request.POST

        # Wir waren auf page 1:
        if "pw1" in req:
            error = False
            # keine Angabe:
            if req.get("email") == "":
                self.context["error1"] = "Bitte geben Sie eine gueltige Email ein!"
                error = True

            if req.get("username") == "":
                error = True
                self.context["error3"] = "Bitte geben Sie einen Benutzernamen ein"
            # versch. Passwörter
            # Tests der Inputs: (To-DO)
            if req.get("pw1") != req.get("pw2"):
                self.context["error3"] = "Passwoerter stimmen nicht ueberein!"
                error = True

            if req.get("pw1") == "":
                self.context["error3"] = "Bitte geben Sie ein gueltiges Passwort ein!"
                error = True

            if len(req.get("pw1")) < 6:
                self.context["error3"] = "Das Passwort muss min. 6 Zeichen lang sein"
                error = True

            if User.objects.filter(username = req.get("username")).exists():
                self.context["error2"] = "Der Benutzername existiert bereits."
                error = True

            if User.objects.filter(email = req.get("email")).exists():
                self.context["error1"] = "Die E-Mail Adresse wird bereits verwendet."
                error = True
            if error:
                return render(request, self.template_name[0], self.context)

            else:# Speichern der "sauberen" inputs in session
                request.session["email"] = req.get("email")
                request.session["pw"] = req.get("pw1")
                request.session["username"] = req.get("username")
                # "jump" to next page
                return render(request, self.template_name[1], self.context)

        # Wir waren auf page 2:
        elif "nname" in req:

            # Tests der Inputs (To-DO)
            error_found = False
            #checkt ob überall Daten gefunden wurden:
            for tag,error in zip(["vname","nname","oname","art","strasse",
                         "hnummer","plz","ort","telnr"], ["error1","error1","error2",
                         "error3","error4","error4","error5","error5","error6"]):

                if (req.get(tag) == "" or req.get(tag) == None) and (tag not in ["telnr"]):
                    error_found = True
                    self.context[error] = "Bitte geben Sie auch diese Daten an:"

            if Organiser.objects.filter(organisation_name = req.get('oname')).exists():
                error_found = True
                self.context['error2'] = "Diese Organisation ist bereits registriert."

            if error_found:
                return render(request, self.template_name[1], self.context)

            for tag in ["vname","nname","oname","art","strasse",
                         "hnummer","plz","ort","telnr"]:
                request.session[tag] = req.get(tag)


            return render(request, self.template_name[2])

        # Wir waren auf page 3:
        elif "iban" in req:


            # Tests der Inputs (To-DO)
            error_found = False
            #checkt ob überall Daten gefunden wurden:
            for tag,error in zip(["kontoinhaber","iban","bic"],
                                 ["error1","error2", "error2"]):

                if (req.get(tag) == "" or req.get(tag) == None):
                    error_found = True
                    self.context[error] = "Bitte geben Sie auch diese Daten an:"

            if error_found:
                return render(request, self.template_name[1], self.context)

            for tag in ["kontoinhaber","iban","bic","kontourl"]:
                request.session[tag] = req.get(tag)


            #To Do: Implementierung der Datenbank
            objetct_useraddress = UserAddress(strasse = request.session["strasse"],
                                  hnummer = request.session["hnummer"],
                                  plz= request.session["plz"],
                                  ort = request.session["ort"],)
            objetct_useraddress.save()
            organiser = Organiser(user_address = objetct_useraddress,
                                  username = request.session["username"],
                                  organisation_name = request.session["oname"],
                                  organisation_type = request.session["art"],
                                  contact_first_name = request.session["vname"],
                                  contact_last_name = request.session["nname"],
                                  contact_phone = request.session["telnr"],
                                  iban = request.session["iban"],
                                  bic = request.session["bic"],
                                  bank_account_owner = request.session["kontoinhaber"],
                                  kontosite = request.session["kontourl"],
                                  email =request.session["email"],)

            organiser.set_password(request.session["pw"])
            organiser.save()
            organiser_user = Organiser.objects.get(username=request.session["username"])
			# user direkt einloggen

            # user = authenticate(request, username=organiser.username, password=organiser.password)
            # if user is not None:
            login(request, organiser_user)
                # return redirect('events:event_organiser_list', Organiser.objects.get(username=username).organisation_name)

            #To Do: Umleitung auf Registrierung erfolgreich
            # Löschen der Sessions IDs:
            for tag in self.tags:
                try:
                    del request.session[tag]
                except KeyError:
                    pass

            return render(request, self.template_name[3], self.context)

        #To DO:
        # Umleitung auf Fehlerseite "Bitte Kontaktieren Sie uns"
        else:
            for tag in self.tags:
                del request.session[tag]
            response = redirect('error/')
            return response
