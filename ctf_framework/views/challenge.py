from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rules.contrib.views import permission_required
from .base_view import *
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from ..models import Solve

from datetime import datetime


@login_required()
def index(request):
    """List all challenges."""

    user = UserProfile.objects.get(user=request.user)
    solved_challenge_ids = [solve.challenge_id for solve in user.solves]
    main_categories = Category.objects.main_categories()

    context = {
        'main_categories': main_categories,
        'solved_challenge_ids': solved_challenge_ids
    }

    return render(request, 'challenge/index.html', context)


@login_required()
def submit(request):
    """Submit a flag for a given challenge."""

    if request.method == "POST":
        user = UserProfile.objects.get(user=request.user)
        flag = request.POST["flag"]

        try:
            # Check for matching challenge with this flag
            challenge = Challenge.objects.get(flag=flag)

            # Add this challenge to user's completed challenges
            solve, created = Solve.objects.get_or_create(user=user, challenge=challenge)

            if created:
                user.last_solve_time = datetime.now()
                user.save()

            messages.success(request, "Correct!")

        except ObjectDoesNotExist:
            messages.warning(request, "Incorrect!")

        # Redirect to challenge#show
        return redirect(reverse("ctf_framework:challenge#index"))


@login_required()
@permission_required('create_challenge')
def new(request):
    """Create a new challenge."""

    context = {
        "form": ChallengeForm()
    }

    return render(request, "challenge/new.html", context)


@login_required()
@permission_required('create_challenge')
def create(request):
    """Save new challenge."""

    if request.method not in "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    form = ChallengeForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Challenge Created!")

    return redirect("ctf_framework:challenge#index")

@login_required()
@permission_required('update_challenge')
def edit(request, challenge_id):
    """Edit an existing challenge."""

    try:
        challenge = Challenge.objects.get(id=challenge_id)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:challenge#index")

    form = ChallengeForm(instance=challenge)

    context = {
        "form": form,
        "challenge_id": challenge_id
    }

    return render(request, "challenge/edit.html", context)


@login_required()
@permission_required('update_challenge')
def update(request, challenge_id):
    """Update existing challenge."""

    if request.method not in "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    try:
        challenge = Challenge.objects.get(id=challenge_id)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:challenge#index")

    form = ChallengeForm(request.POST, instance=challenge)
    if form.is_valid():
        form.save()
        messages.success(request, "Challenge Updated!")

    return redirect("ctf_framework:challenge#index")


@login_required()
@permission_required('delete_challenge')
def delete(request, challenge_id):

    if request.method in "GET":
        try:
            challenge = Challenge.objects.get(id=challenge_id)
        except ObjectDoesNotExist:
            return redirect("ctf_framework:challenge#index")

        return render(request, "challenge/delete.html", {"challenge": challenge})

    if request.method in "POST":
        try:
            Challenge.objects.get(id=challenge_id).delete()
        except ObjectDoesNotExist:
            pass

    return redirect("ctf_framework:challenge#index")
