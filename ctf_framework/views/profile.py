from .base_view import *
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib import messages


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
        "completed_challenges": user.get_completed_challenges(),
        "can_edit": request_user_profile == user_profile or request_user_profile.is_admin
    }
    return render(request, "profile/show.html", context)


def logout(request):
    """Logout user."""

    django_logout(request)
    return redirect("ctf_framework:home#index")


def edit(request, user_id):
    """Edit User Profile."""
    try:
        user_profile = UserProfile.objects.get(id=user_id)
        request_user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:home#index")

    # Verify user editing their own profile or they are an admin
    if request_user_profile != user_profile and not request_user_profile.is_admin:
        return HttpResponseForbidden()

    if request_user_profile.is_admin:
        form = UserProfileAdminForm(instance=user_profile)
    else:
        form = UserProfileForm(instance=user_profile)

    context = {"form": form,
               "user_id": user_id}

    return render(request, "profile/edit.html", context)


def update(request, user_id):
    """Update User Profile."""
    try:
        user_profile = UserProfile.objects.get(id=user_id)
        request_user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:home#index")

    # Verify user editing their own profile or they are an admin
    if request_user_profile != user_profile and not request_user_profile.is_admin:
        return HttpResponseForbidden()

    if request_user_profile.is_admin:
        form = UserProfileAdminForm(request.POST, instance=user_profile)
    else:
        form = UserProfileForm(request.POST, instance=user_profile)

    form.save()
    messages.success(request, "Profile Updated!")

    return redirect("ctf_framework:profile#show", user_id)








