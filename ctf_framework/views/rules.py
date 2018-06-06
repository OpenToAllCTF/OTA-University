from .base_view import *
from django.contrib import messages


def index(request):
    return render(request, "misc/rules.html")
