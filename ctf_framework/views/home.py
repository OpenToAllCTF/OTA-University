from .base_view import *


def index(request):
    """View the home page."""

    users = UserProfile.objects.all().prefetch_related('solve_set') \
                                     .prefetch_related('solve_set__challenge') \
                                     .select_related('active_title')

    # Order users by score and last_solve_time
    sorted_users = sorted(users, key=lambda u: (-u.score, u.last_solve_time))
    context = { "users": sorted_users }

    return render(request, "misc/home.html", context=context)
