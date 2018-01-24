from django.http import HttpResponse
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .models import UserProfile, Challenge


# Create your views here.


def home(request):
    users = UserProfile.objects.all()
    challenges = Challenge.objects.all()

    context = {
        "users": users,
        "challenges": challenges
    }

    return render(request, "misc/home.html", context=context)


def profile(request, user_id=None):
    user = UserProfile.objects.get(id=user_id)
    context = {
        "user": user,
        "completed_challenges": user.get_completed_challenges()
    }
    return render(request, "profile/show.html", context)


def challenge(request, challenge_id):
    user = UserProfile.objects.get(user=request.user)
    message = None

    if request.method == "POST":
        flag = request.POST["flag"]
        try:
            # Check for matching challenge with this flag
            _challenge = Challenge.objects.get(id=challenge_id, flag=flag)

            # Add this challenge to user's completed challenges
            user.challenges.add(_challenge)
            user.save()
            message = "Correct!"

        except ObjectDoesNotExist:
            message = "Incorrect!"

    _challenge = Challenge.objects.get(id=challenge_id)

    context = {
        "challenge": _challenge,
        "user": user,
        "challenge_completed": _challenge in user.challenges.all(),
        "message": message
    }

    return render(request, "challenge/show.html", context)


def logout(request):
    django_logout(request)
    return redirect("ctf_framework:home")






