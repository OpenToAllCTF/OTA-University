from django.contrib import admin
from .models import UserProfile, Title, Challenge, Category, Writeup

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Title)
admin.site.register(Challenge)
admin.site.register(Category)
admin.site.register(Writeup)
