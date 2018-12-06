from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .base_view import *
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from ..models import Solve

@login_required()
def index(request):
    """Get some solves metrics."""

    solves = Solve.objects.all()

    context = {"solves": solves}
    return render(request, "analytics/index.html", context)
