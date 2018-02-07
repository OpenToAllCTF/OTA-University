from .models import Challenge
from django.forms import ModelForm


class ChallengeForm(ModelForm):
    class Meta:
        model = Challenge
        fields = ["name", "description", "category", "point_value", "url", "is_active", "flag"]
