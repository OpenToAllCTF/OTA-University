from django import template
from ..models import UserProfile, Challenge, Category, Writeup, Solve

register = template.Library()


@register.filter(name='get_user_display_name')
def get_user_display_name(uid):
    try:
        user = UserProfile.objects.get(id=uid)
    except:
        return 'N/A'
    return user.display_name if user else 'N/A'


@register.filter(name='get_challenge_name')
def get_challenge_name(uid):
    try:
        chall = Challenge.objects.get(id=uid)
    except:
        return 'N/A'
    return chall.name if chall else 'N/A'
