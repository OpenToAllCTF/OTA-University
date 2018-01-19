from .base_view import *

def show(request, challenge_id):
    """View the page of a specific challenge."""
    user = UserProfile.objects.get(user=request.user)
    message = None

    challenge = Challenge.objects.get(id=challenge_id)

    context = {
        "challenge": challenge,
        "user": user,
        "challenge_completed": challenge in user.challenges.all(),
        "message": message
    }

    return render(request, "challenge/show.html", context)

def submit(request, challenge_id):
    """Submit a flag for a given challenge."""

    user = UserProfile.objects.get(user=request.user)
    message = None

    challenge = Challenge.objects.get(id=challenge_id)

    if request.method == "POST":
        flag = request.POST["flag"]
        try:
            # Check for matching challenge with this flag
            challenge = Challenge.objects.get(id=challenge_id, flag=flag)

            # Add this challenge to user's completed challenges
            user.challenges.add(challenge)
            user.save()
            message = "Correct!"

        except ObjectDoesNotExist:
            message = "Incorrect!"

    context = {
        "challenge": challenge,
        "user": user,
        "challenge_completed": challenge in user.challenges.all(),
        "message": message
    }

    return render(request, "challenge/show.html", context)

