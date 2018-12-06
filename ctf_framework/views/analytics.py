from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .base_view import *
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from ..models import Solve


@login_required()
def index(request):
    """List all active Categories."""
    if not request.user.is_staff:
        return HttpResponseForbidden()

    solves = Solve.objects.all().reverse()#[:1000] # last 1000 entries
    context = {"solves": solves}

    return render(request, "analytics/index.html", context)
