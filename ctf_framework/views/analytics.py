from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .base_view import *
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from ..models import Solve
from django.utils import timezone
from datetime import timedelta

@login_required()
def index(request):
    """List analytics."""

    solves = Solve.objects.prefetch_related('challenge', 'user')

    chart_data = {}
    now = timezone.now()

    for category in Category.objects.all():
        chart_data[category] = []

        for offset in range(7):
            end = now - timedelta(days=offset)
            start = now - timedelta(days=offset + 1)
            solve_count = len([solve for solve in solves if solve.is_between_dates(start, end) and solve.challenge.category_id == category.id])
            chart_data[category].append(solve_count)

    context = {
        "solves": solves,
        # "chart_data": solves_chart_data
    }

    return render(request, "analytics/index.html", context)

@login_required
def latest_solves(request):

    solves = Solve.objects.prefetch_related('challenge', 'user', 'challenge__category')

    solves_json = []
    for solve in solves:
        solves_json.append({
            'id': solve.id,
            'user': solve.user.display_name,
            'challenge': solve.challenge.name,
            'category': solve.challenge.category.name,
            'points': solve.challenge.point_value,
            'date': solve.date.strftime('%Y-%m-%S %T')
        })

    return JsonResponse({ 'data': solves_json })
