from .models import Challenge, UserProfile, ChallengeCategory, Title
from django.forms import ModelForm


class ChallengeForm(ModelForm):
    class Meta:
        model = Challenge
        fields = ["name", "author", "description", "category", "url", "is_active", "flag"]


class ChallengeCategoryForm(ModelForm):
    class Meta:
        model = ChallengeCategory
        fields = ["category", "description"]


class TitleForm(ModelForm):
    class Meta:
        model = Title
        fields = ["title"]


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["active_title"]


class UserProfileAdminForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ["active_title"]
