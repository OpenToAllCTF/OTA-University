from django.urls import path

from .views import *

# Used for URL namespacing in templates
app_name = "ctf_framework"

urlpatterns = [
    # Misc
    path('', home.index, name="home#index"),

    # Profile
    path('profile/<int:user_id>/', profile.show, name="profile#show"),
    path("profile/logout", profile.logout, name="profile#logout"),

    # Challenge
    path('challenges/', challenge.index, name="challenge#index"),
    path('challenge/submit', challenge.submit, name="challenge#submit"),

    # Writeups
    path('challenge/<int:challenge_id>/writeups', writeup.index, name="writeup#index"),
    path('writeups/submit', writeup.submit, name="writeup#submit"),
    path('writeup/<int:writeup_id>', writeup.show, name="writeup#show"),
    path('writeup/<int:writeup_id>/edit', writeup.edit, name="writeup#edit"),

]
