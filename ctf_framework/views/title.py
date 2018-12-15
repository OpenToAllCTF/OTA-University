from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rules.contrib.views import permission_required
from .base_view import *
from django.http import HttpResponseForbidden, HttpResponseNotAllowed


@login_required()
@permission_required('manage_titles')
def index(request):
    """List all active Categories."""
    titles = Title.objects.all()

    context = { "titles": titles }
    return render(request, "title/index.html", context)


@login_required()
@permission_required('manage_titles')
def new(request):
    """Create a new title."""

    context = {
        "form": TitleForm()
    }

    return render(request, "title/new.html", context)


@login_required()
@permission_required('manage_titles')
def create(request):
    """Save new title."""

    if request.method not in "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    form = TitleForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Title Created!")

    return redirect("ctf_framework:title#index")


@login_required()
@permission_required('manage_titles')
def edit(request, title_id):
    """Edit an existing title."""

    try:
        title = Title.objects.get(id=title_id)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:title#index")

    form = TitleForm(instance=title)

    context = {
        "form": form,
        "title_id": title_id
    }

    return render(request, "title/edit.html", context)


@login_required()
@permission_required('manage_titles')
def update(request, title_id):
    """Update existing challenge."""

    if request.method not in "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    try:
        title = Title.objects.get(id=title_id)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:title#index")

    form = TitleForm(request.POST, instance=title)
    if form.is_valid():
        form.save()
        messages.success(request, "Title Updated!")

    return redirect("ctf_framework:title#index")
