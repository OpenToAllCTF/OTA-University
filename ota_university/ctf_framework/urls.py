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
    path('challenge/<int:challenge_id>/', challenge.submit, name="challenge#submit"),
    path('challenge/<int:challenge_id>/', challenge.show, name="challenge#show")
]
