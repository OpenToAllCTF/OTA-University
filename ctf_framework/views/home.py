from .base_view import *


def index(request):
    """View the home page."""

    users = UserProfile.objects.all()
    challenges = Challenge.objects.all()

    # Order users by score
    sorted_users = sorted(users, key=lambda u: -u.get_score())

    context = {
        "users": sorted_users,
        "challenges": challenges
    }

    return render(request, "misc/home.html", context=context)
