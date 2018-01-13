from .base_view import *
def index(request):
    users = UserProfile.objects.all()
    challenges = Challenge.objects.all()

    context = {
        "users": users,
        "challenges": challenges
    }

    return render(request, "misc/home.html", context=context)


