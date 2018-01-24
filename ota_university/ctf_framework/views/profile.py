from .base_view import *


def show(request, user_id):
    """View a page for a single profile."""
    user = UserProfile.objects.get(id=user_id)
    context = {
        "user": user,
        "completed_challenges": user.get_completed_challenges()
    }
    return render(request, "profile/show.html", context)


def logout(request):
    """ Logout user. """
    django_logout(request)
    return redirect("ctf_framework:home#index")

