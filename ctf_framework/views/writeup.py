from django.contrib.auth.decorators import login_required
from .base_view import *
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.utils.safestring import mark_safe
from markdown import markdown
from bleach import clean

markdown_tags = [
    "h1", "h2", "h3", "h4", "h5", "h6",
    "b", "i", "strong", "em", "tt",
    "p", "br",
    "span", "div", "blockquote", "code", "hr", "pre",
    "ul", "ol", "li", "dd", "dt",
    "img",
    "a",
]

markdown_attrs = {
    "img": ["src", "alt", "title"],
    "a": ["href", "alt", "title"],
    "*": ["class"],
}

@login_required()
def index(request, challenge_id):
    """List all writeups for a challenge."""

    user = UserProfile.objects.get(user=request.user)
    challenge = Challenge.objects.get(id=challenge_id)

    if challenge in user.completed_challenges.all():
        writeups = Writeup.objects.filter(challenge_id=challenge_id)
        writeup = Writeup.objects.filter(user=user.user, challenge=challenge).first()
        context = {
            "challenge": challenge,
            "writeups": writeups,
            "writeup": writeup
        }
        return render(request, "writeup/index.html", context)
    else:
        return HttpResponseForbidden("You must solve the challenge first")



@login_required()
def show(request, writeup_id):
    """View the page of a specific writeup."""

    user = UserProfile.objects.get(user=request.user)
    writeup = Writeup.objects.get(id=writeup_id)
    challenge = Challenge.objects.get(id=writeup.challenge.id)
    html = clean(
        markdown(writeup.markdown, extensions=['markdown.extensions.fenced_code', 'markdown.extensions.codehilite']),
        markdown_tags,
        markdown_attrs
    )

    if challenge in user.completed_challenges.all():
        context = {
            "writeup": writeup,
            "html": mark_safe(html)
        }
        return render(request, "writeup/show.html", context)
    else:
        return HttpResponseForbidden("You must solve the challenge first")


@login_required()
def edit(request, writeup_id):
    """Edit the existing writeup for a given challenge."""

    if request.method == "POST":
        user = UserProfile.objects.get(user=request.user)
        writeup = Writeup.objects.get(id=writeup_id)
        challenge = Challenge.objects.get(id=writeup.challenge.id)

        if user.user == writeup.user and challenge in user.completed_challenges.all():
            writeup = Writeup.objects.get(id=writeup_id)
            writeup.markdown = request.POST["markdown"]
            writeup.save()

            return redirect(reverse("ctf_framework:writeup#show", args=[writeup.id]))
        else:
            return HttpResponseForbidden("You must solve the challenge first")

@login_required()
def submit(request):
    """Create a new writeup for a given challenge."""

    if request.method == "POST":
        user = UserProfile.objects.get(user=request.user)
        challenge = Challenge.objects.get(id=request.POST["challenge"])

        if challenge in user.completed_challenges.all():
            writeup = Writeup.objects.create(user=user.user, challenge=challenge, markdown=request.POST["markdown"])
            writeup.save()

            return redirect(reverse("ctf_framework:writeup#show", args=[writeup.id]))
        else:
            return HttpResponseForbidden("You must solve the challenge first")
