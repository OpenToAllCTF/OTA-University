from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .base_view import *
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed


@login_required()
def index(request):
    """List all active Categories."""
    if not request.user.is_staff:
        return HttpResponseForbidden()

    categories = [category for category in Category.objects.all() if not category.parent]
    context = { "categories": categories }

    return render(request, "category/index.html", context)


@login_required()
def new(request):
    """Create a new category."""

    if not request.user.is_staff:
        return HttpResponseForbidden()

    context = { "form": CategoryForm() }

    return render(request, "category/new.html", context)


@login_required()
def create(request):
    """Save new category."""

    if not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method not in "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    form = CategoryForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "Category Created!")

    return redirect("ctf_framework:category#index")


@login_required()
def edit(request, category_id):
    """Edit an existing category."""

    if not request.user.is_staff:
        return HttpResponseForbidden()

    try:
        category = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:category#index")

    context = {
        "form": CategoryForm(instance=category),
        "category_id": category_id
    }

    return render(request, "category/edit.html", context)


@login_required()
def update(request, category_id):
    """Update existing challenge."""

    if not request.user.is_staff:
        return HttpResponseForbidden()

    if request.method not in "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    try:
        category = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:category#index")

    form = CategoryForm(request.POST, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, "Category Updated!")

    return redirect("ctf_framework:category#index")
