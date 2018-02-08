from .models import Challenge, UserProfile
from django.forms import ModelForm


class ChallengeForm(ModelForm):
    class Meta:
        model = Challenge
        fields = ["name", "description", "category", "point_value", "url", "is_active", "flag"]


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["active_title"]


class UserProfileAdminForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["titles", "active_title", "completed_challenges", "is_admin"]
