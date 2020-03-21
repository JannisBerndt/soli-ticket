# -*- coding: cp1252 -*-
from .forms import RegisterForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View



class Register(View):
    template_name = ['register/register_start.html',
                     'register/register_start2.html',
                     'register/register_start3.html',]
    context = {"error1" : "",
               "error2" : "",
               "error3" : "",
               "error4" : "",
               "error5" : "",
               "error6" : "",}
    tags = ["email","pw","vname","nname","oname","art","strasse",
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

            # Tests der Inputs: (To-DO)
            if req.get("pw1") != req.get("pw2"):
                self.context["error2"] = "Passw�rter stimmen nicht �berein"
                return render(request, self.template_name[0], self.context)


            # Speichern der "sauberen" inputs in session
            request.session["email"] = req.get("email")
            request.session["pw"] = req.get("pw1")

            # "jump" to next page
            return render(request, self.template_name[1], self.context)

        # Wir waren auf page 2:
        elif "nname" in req:

            # Tests der Inputs (To-DO)

            for tag in ["vname","nname","oname","art","strasse",
                         "hnummer","plz","ort","telnr"]:
                request.session[tag] = req.get(tag)


            return render(request, self.template_name[2])

        # Wir waren auf page 3:
        elif "iban" in req:
           # Tests der Inputs (To-DO)
            for tag in ["kontoinhaber","iban","bic","kontourl"]:
                request.session[tag] = req.get(tag)
            for tag in self.tags:
                print(tag ,':', request.session[tag])
            #To Do: Umleitung auf Registrierung erfolgreich
            #To Do: Implementierung der Datenbank
            return render(request, self.template_name[0], self.context)
        #To DO:
        # Umleitung auf Fehlerseite "Bitte Kontaktieren Sie uns"
        #else:
        #    return Fehler
