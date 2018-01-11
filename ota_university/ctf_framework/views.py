from django.http import HttpResponse
from django.shortcuts import render
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
    return HttpResponse("""
    User: {}<br>
    Title: {}<br>
    Score: {}<br>
    """.format(user, user.active_title, user.get_score()))


