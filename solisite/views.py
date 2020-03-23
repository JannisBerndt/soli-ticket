from django.shortcuts import render, redirect

def landingpage_view(request):
    context = {

    }
    return render(request, 'solisite/landingpage.html', context)

def about_view(request):
	context = {

	}
	return render(request, 'solisite/about.html', context)

def imprint_view(request):
	context = {

	}
	return render(request, 'solisite/imprint.html', context)

def privacy_policy_view(request):
	context = {

	}
	return render(request, 'solisite/privacy_policy.html', context)