from accounts.models import Organiser

def organiser_user(request):
    if hasattr(request, 'user'):
        user = request.user
        organiser_user = Organiser.objects.get(username=user.username)
    else:
        from django.contrib.auth.models import AnonymousUser
        organiser_user = None

    return {
        'organiser_user': organiser_user,
    }