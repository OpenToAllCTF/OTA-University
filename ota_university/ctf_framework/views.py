from django.http import HttpResponse
from django.shortcuts import render
from .models import UserProfile

# Create your views here.


def home(request):
    user = UserProfile.objects.all()[0]
    return HttpResponse("""
    User: {}<br>
    Title: {}<br>
    Score: {}<br>
    """.format(user, user.active_title, user.get_score()))
