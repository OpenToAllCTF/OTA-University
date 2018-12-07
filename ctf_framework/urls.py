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
    path("profile/<int:user_id>/title/<int:title_id>/delete", profile.delete_title, name="profile#delete_title"),
    path("profile/<int:user_id>/title/add", profile.add_title, name="profile#add_title"),

    # Challenge
    path('challenges/', challenge.index, name="challenge#index"),
    path('challenge/submit', challenge.submit, name="challenge#submit"),
    path('challenge/new', challenge.new, name="challenge#new"),
    path('challenge/create', challenge.create, name="challenge#create"),
    path('challenge/<int:challenge_id>/edit', challenge.edit, name="challenge#edit"),
    path('challenge/<int:challenge_id>/update', challenge.update, name="challenge#update"),
    path('challenge/<int:challenge_id>/delete', challenge.delete, name="challenge#delete"),

    # Category
    path('categories/', category.index, name="category#index"),
    path('category/new', category.new, name="category#new"),
    path('category/create', category.create, name="category#create"),
    path('category/<int:category_id>/edit', category.edit , name="category#edit"),
    path('category/<int:category_id>/update', category.update, name="category#update"),

    # Title
    path('titles/', title.index, name="title#index"),
    path('title/new', title.new, name="title#new"),
    path('title/create', title.create, name="title#create"),
    path('title/<int:title_id>/edit', title.edit, name="title#edit"),
    path('title/<int:title_id>/update', title.update, name="title#update"),

    # Writeups
    path('challenge/<int:challenge_id>/writeups', writeup.index, name="writeup#index"),
    path('writeups/submit', writeup.submit, name="writeup#submit"),
    path('writeup/<int:writeup_id>', writeup.show, name="writeup#show"),
    path('writeup/<int:writeup_id>/edit', writeup.edit, name="writeup#edit"),

    # Rules
    path("rules", rules.index, name="rules#index"),

    # Analytics
    path("analytics/", analytics.index, name='analytics#index'),
    path("analytics/latest_solves.json", analytics.latest_solves, name='analytics#latest_solves'),
    path("analytics/last_week.json", analytics.last_week, name='analytics#last_week'),
]
