from django.contrib.auth.decorators import login_required
from .base_view import *


@login_required()
def index(request):
    """List all active challenges."""

    user = UserProfile.objects.get(user=request.user)
    challenges = Challenge.objects.filter(is_active=True)

    challenge_context = []

    for challenge in challenges:
        challenge_context.append({"challenge": challenge, "is_completed": challenge in user.completed_challenges.all()})

    context = {
        "challenges": challenge_context
    }
    return render(request, "challenge/index.html", context)


@login_required()
def show(request, challenge_id, message=None):
    """View the page of a specific challenge."""

    user = UserProfile.objects.get(user=request.user)
    challenge = Challenge.objects.get(id=challenge_id)

    context = {
        "challenge": challenge,
        "user": user,
        "challenge_completed": challenge in user.completed_challenges.all(),
        "message": message
    }

    return render(request, "challenge/show.html", context)


@login_required()
def submit(request, challenge_id):
    """Submit a flag for a given challenge."""

    if request.method == "POST":
        user = UserProfile.objects.get(user=request.user)
        flag = request.POST["flag"]

        try:
            # Check for matching challenge with this flag/
            challenge = Challenge.objects.get(id=challenge_id, flag=flag)

            # Add this challenge to user's completed challenges/
            user.completed_challenges.add(challenge)
            user.save()
            message = "Correct!"

        except ObjectDoesNotExist:
            message = "Incorrect!"

        # Return the show view with a response message.
        return show(request, challenge_id, message)
