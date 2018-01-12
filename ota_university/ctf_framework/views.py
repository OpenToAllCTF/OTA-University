from django.http import HttpResponse
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from .models import UserProfile, Challenge


# Create your views here.


def home(request):
    users = UserProfile.objects.all()
    challenges = Challenge.objects.all()

    context = {
        "users": users,
        "challenges": challenges
    }

    return render(request, "home.html", context=context)


def profile(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    context = {
        "user": user,
        "completed_challenges": user.get_completed_challenges()
    }
    return render(request, "profile.html", context)


def challenge(request, challenge_id):
    user = UserProfile.objects.get(user=request.user)
    challenge = Challenge.objects.get(id=challenge_id)

    context = {
        "challenge": challenge,
        "user": user,
        "challenge_completed": challenge in user.challenges.all()
    }

    return render(request, "challenge.html", context)


def logout(request):
    django_logout(request)
    return redirect("ctf_framework:home")






