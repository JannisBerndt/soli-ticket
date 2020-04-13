"""solisite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import landingpage_view, privacy_policy_view, imprint_view, about_view, blog_view, faq_view, agb_view, oauth_view, contact_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landingpage_view, name='home'),
	path('privacy_policy/', privacy_policy_view, name='privacy_policy'),
	path('imprint/', imprint_view, name='imprint'),
	path('about/', about_view, name='about'),
    path('accounts/', include('accounts.urls')),
    path('event/', include('events.urls')),
	path('payment/', include('payment.urls')),
    path('blog/', blog_view, name='blog'),
	path('faq/', faq_view, name='faq'),
    path('agb/', agb_view, name='agb'),
    path('oauth/', oauth_view, name = 'oauth'),
    path('contact/', contact_view, name='contact'),
]
