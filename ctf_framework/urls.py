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
    path("profile/<int:user_id>/edit", profile.edit, name="profile#edit"),
    path("profile/<int:user_id>/update", profile.update, name="profile#update"),

    # Challenge
    path('challenges/', challenge.index, name="challenge#index"),
    path('challenge/submit', challenge.submit, name="challenge#submit"),
    path('challenge/new', challenge.new, name="challenge#new"),
    path('challenge/create', challenge.create, name="challenge#create"),
    path('challenge/<int:challenge_id>/edit', challenge.edit, name="challenge#edit"),
    path('challenge/<int:challenge_id>/update', challenge.update, name="challenge#update"),

    # Writeups
    path('challenge/<int:challenge_id>/writeups', writeup.index, name="writeup#index"),
    path('writeups/submit', writeup.submit, name="writeup#submit"),
    path('writeup/<int:writeup_id>', writeup.show, name="writeup#show"),
    path('writeup/<int:writeup_id>/edit', writeup.edit, name="writeup#edit"),

]
