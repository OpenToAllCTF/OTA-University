from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .base_view import *
from rules.contrib.views import permission_required
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotAllowed


@login_required()
@permission_required('manage_categories')
def index(request):
    """List all active Categories."""

    categories = [category for category in Category.objects.all() if not category.parent]
    context = { "categories": categories }

    return render(request, "category/index.html", context)


@login_required()
@permission_required('manage_categories')
def new(request):
    """Create a new category."""

    context = {
        'form': CategoryForm(),
        'categories': Category.objects.all()
    }

    return render(request, "category/new.html", context)


@login_required()
@permission_required('manage_categories')
def create(request):
    """Save new category."""

    if request.method not in "POST":
        return HttpResponseNotAllowed(permitted_methods=["POST"])

    form = CategoryForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(request, "Category Created!")

    return redirect("ctf_framework:category#index")


@login_required()
@permission_required('manage_categories')
def edit(request, category_id):
    """Edit an existing category."""

    try:
        category = Category.objects.get(id=category_id)
    except ObjectDoesNotExist:
        return redirect("ctf_framework:category#index")

    context = {
        "form": CategoryForm(instance=category),
        "category": category,
        'categories': Category.objects.all()
    }

    return render(request, "category/edit.html", context)


@login_required()
@permission_required('manage_categories')
def update(request, category_id):
    """Update existing challenge."""

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
