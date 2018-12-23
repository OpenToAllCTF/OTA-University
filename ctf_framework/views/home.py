from .base_view import *


def index(request):
    """View the home page."""

    users = UserProfile.objects.all().prefetch_related('solve_set','solve_set__challenge')

    # Order users by score and last_solve_time
    sorted_users = sorted(users, key=lambda u: (-u.score, u.last_solve_time))

    rankings = []
    current_rank = 0
    rankings_to_skip = 1
    previous_score = None
    for user in sorted_users:

        if user.score != previous_score:
            previous_score = user.score
            current_rank += rankings_to_skip
            rankings_to_skip = 1
        else:
            rankings_to_skip += 1

        rankings.append(current_rank)

    context = { "users": zip(rankings, sorted_users) }

    return render(request, "misc/home.html", context=context)
