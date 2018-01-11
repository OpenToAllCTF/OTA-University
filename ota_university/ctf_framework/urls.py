from django.urls import path, include

from .views import *

# Used for URL namespacing in templates
app_name = "ctf_framework"

urlpatterns = [
    path('', home, name="home"),
    path('profile/<int:user_id>/', profile, name="profile")
]
