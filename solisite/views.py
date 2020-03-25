from django.shortcuts import render, redirect

def landingpage_view(request):
    try:
        organiser_user = Organiser.objects.get(username = request.user.username)
    except:
        organiser_user = None
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
