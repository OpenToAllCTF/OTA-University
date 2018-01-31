from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .base_view import *
from django.urls import reverse


@login_required()
def index(request):
    """List all active challenges."""

    user = UserProfile.objects.get(user=request.user)
    challenges = Challenge.objects.filter(is_active=True)

    categories = {}

    for challenge in challenges:
        category = challenge.category
        challenge_list = categories.get(category, [])
        challenge_list.append({
            "challenge" : challenge,
            "is_completed" : challenge in user.completed_challenges.all()
        })
        categories[category] = challenge_list

    context = { "categories": categories }
    return render(request, "challenge/index.html", context)

@login_required()
def submit(request):
    """Submit a flag for a given challenge."""

    if request.method == "POST":
        user = UserProfile.objects.get(user=request.user)
        flag = request.POST["flag"]

        try:
            # Check for matching challenge with this flag
            challenge = Challenge.objects.get(flag=flag)

            # Add this challenge to user's completed challenges
            user.completed_challenges.add(challenge)
            user.save()
            messages.success(request, "Correct!")

        except ObjectDoesNotExist:
            messages.warning(request, "Incorrect!")

        # Redirect to challenge#show
        return redirect(reverse("ctf_framework:challenge#index"))
