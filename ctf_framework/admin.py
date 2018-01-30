from django.contrib import admin
from .models import UserProfile, Title, Challenge, ChallengeCategory, Writeup

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Title)
admin.site.register(Challenge)
admin.site.register(ChallengeCategory)
admin.site.register(Writeup)