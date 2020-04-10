from accounts.models import Organiser

def organiser_user(request):
    if hasattr(request, 'user'):
        user = request.user
        try:
            organiser_user = Organiser.objects.get(username=user.username)
        except:
            organiser_user = None
    else:
        organiser_user = None

    return {
        'organiser_user': organiser_user,
    }