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
    """View analytics."""

    return render(request, "analytics/index.html")

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
            'date': solve.date.strftime('%Y-%m-%d %T')
        })

    return JsonResponse({ 'data': solves_json })

@login_required
def last_week(request):

    solves = Solve.objects.prefetch_related('challenge', 'user')
    categories = [category for category in Category.objects.all() if not category.parent]

    chart_data = {}
    now = timezone.now()

    for category in categories:
        chart_data[category.name] = []

        for offset in reversed(range(7)):

            end = now - timedelta(days=offset)
            start = now - timedelta(days=offset + 1)

            solve_count = len([solve for solve in solves if solve.is_between_dates(start, end) and solve.belongs_to_category(category)])
            chart_data[category.name].append(solve_count)

    output = {
        'categories': list(chart_data.keys()),
        'labels': ["{} days ago".format(i) for i in reversed(range(2, 7))] + ["1 day ago", ""],
        'data': chart_data
    }

    return JsonResponse(output)
