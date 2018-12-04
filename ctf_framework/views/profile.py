from django.contrib.auth.decorators import login_required
from .base_view import *
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib import messages
from ..models import TitleGrant


@login_required()
def show(request, user_id):
    """View a page for a single profile."""

    try:
        user_profile = UserProfile.objects.get(id=user_id)
        request_user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:home#index")

    user = UserProfile.objects.get(id=user_id)
    context = {
        "user": user,
        "solves": reversed(user.solves),
        "can_edit": request_user_profile == user_profile or request_user_profile.is_staff
    }

    return render(request, "profile/show.html", context)


def logout(request):
    """Logout user."""

    django_logout(request)
    return redirect("ctf_framework:home#index")


@login_required()
def edit(request, user_id):
    """Edit User Profile."""
    try:
        user_profile = UserProfile.objects.get(id=user_id)
        request_user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:home#index")

    # Verify user editing their own profile or they are an admin
    if request_user_profile != user_profile and not request_user_profile.is_staff:
        return HttpResponseForbidden()

    if request_user_profile.is_staff:
        form = UserProfileAdminForm(instance=user_profile)
    else:
        form = UserProfileForm(instance=user_profile)
        form.fields["active_title"].queryset = user_profile.earned_titles

    context = {
        "form": form,
        "user": user_profile
    }

    # Get all titles that the user doesn't currently have available
    if request.user.is_staff:
        context["unearned_titles"] = user_profile.missing_titles
        return render(request, "profile/edit_admin.html", context)
    return render(request, "profile/edit.html", context)


@login_required()
def update(request, user_id):
    """Update User Profile."""
    try:
        user_profile = UserProfile.objects.get(id=user_id)
        request_user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:home#index")

    # Verify user editing their own profile or they are an admin
    if request_user_profile != user_profile and not request_user_profile.is_staff:
        return HttpResponseForbidden()

    if request_user_profile.is_staff:
        # Staff can set anyone to any title

        form = UserProfileAdminForm(request.POST, instance=user_profile)
        form.save()
        messages.success(request, "Profile Updated!")

    else:
        try:
            requested_title_id = request.POST["active_title"]
            if requested_title_id in "":
                requested_title_id = 0
            requested_title = Title.objects.get(id=requested_title_id)

        except ObjectDoesNotExist:
            # Covers setting title to None and requesting invalid titles
            user_profile.active_title = None
            user_profile.save()
            messages.success(request, "Profile Updated!")
            return redirect("ctf_framework:profile#show", user_id)

        if requested_title not in user_profile.earned_titles.all():
            # Bad Title ID requested
            messages.warning(request, "HAXOR!")

        else:
            form = UserProfileForm(request.POST, instance=user_profile)
            form.save()
            messages.success(request, "Profile Updated!")

    return redirect("ctf_framework:profile#show", user_id)


@login_required()
def add_title(request, user_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    try:
        user_profile = UserProfile.objects.get(id=user_id)
        title = Title.objects.get(id=request.POST["title"])
    except ObjectDoesNotExist:
        return redirect("ctf_framework:home#index")

    # Create if doesn't exist
    TitleGrant.objects.get_or_create(user=user_profile, title=title)

    return redirect("ctf_framework:profile#edit", user_id)


@login_required()
def delete_title(request, user_id, title_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    try:
        user_profile = UserProfile.objects.get(id=user_id)
        title = Title.objects.get(id=title_id)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:home#index")

    try:
        TitleGrant.objects.get(user=user_profile, title=title).delete()
    except ObjectDoesNotExist:
        pass

    return redirect("ctf_framework:profile#edit", user_id)
