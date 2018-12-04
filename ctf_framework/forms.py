from .models import Challenge, UserProfile, Category, Title
from django.forms import ModelForm


class ChallengeForm(ModelForm):
    class Meta:
        model = Challenge
        fields = [
            "name", "author", "description", "category",
            "connection_info", "is_active", "flag"
        ]

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description", "parent"]


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
