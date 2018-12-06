from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .base_view import *
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from ..models import Solve
from django.utils import timezone
from datetime import timedelta

@login_required()
def index(request):
    """Get some solves metrics."""

    solves = Solve.objects.prefetch_related('challenge', 'user')

    solves_chart_data = {}

    for category in ['Misc', 'Web', 'Pwn', 'Forensics', 'Reverse Engineering', 'Crypto']:
        if category not in solves_chart_data:
            solves_chart_data[category] = []

        # 1 day ago
        delta_a = timezone.now() - timedelta(days=1)
        solves_chart_data[category].append(
            solves.filter(date__gte=delta_a, challenge__category__name=category).count() )

        # 2 days before that
        delta_b = delta_a - timedelta(days=1)
        solves_chart_data[category].append(
            solves.filter(date__gte=delta_b, date__lt=delta_a, challenge__category__name=category).count() )

        # 5 days before that 
        for _ in range(5):
            delta_a = delta_b
            delta_b = delta_a - timedelta(days=1)
            solves_chart_data[category].append(
                solves.filter(date__gte=delta_b, date__lt=delta_a, challenge__category__name=category).count() )

    context = {
        "solves": solves,
        # "chart_data": solves_chart_data
    }
    
    return render(request, "analytics/index.html", context)
