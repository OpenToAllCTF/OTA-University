from django.contrib.auth.decorators import login_required
from .base_view import *
from django.urls import reverse
from django.http import HttpResponseForbidden, HttpResponseNotFound
from django.utils.safestring import mark_safe
from markdown import markdown
from bleach import clean
from bleach_whitelist import markdown_attrs, markdown_tags

safe_tags = set(markdown_tags + ["table", "thead", "tbody", "tfoot", "tr", "th", "td", "pre"])

safe_attrs = {"*": ["class", "style"]}
safe_attrs.update(markdown_attrs)

@login_required()
def index(request, challenge_id):
    """List all writeups for a challenge."""

    profile = UserProfile.objects.get(user_id=request.user.id)
    challenge = Challenge.objects.get(id=challenge_id)

    if request.user.has_perm('read_writeups_for_challenge', challenge):
        writeups = Writeup.objects.filter(challenge_id=challenge.id)
        writeup = Writeup.objects.filter(user_id=profile.id, challenge=challenge).first()
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

    profile = UserProfile.objects.get(user=request.user)

    try:
        writeup = Writeup.objects.get(id=writeup_id)
    except:
        return HttpResponseNotFound("Writeup not found")

    challenge = Challenge.objects.get(id=writeup.challenge.id)
    html = clean(
        markdown(
            writeup.markdown,
            extensions=['markdown.extensions.fenced_code', 'markdown.extensions.codehilite'],
            extension_configs={ "markdown.extensions.codehilite": { "linenums": False }}
        ),
        safe_tags,
        safe_attrs
    )

    if request.user.has_perm('read_writeups_for_challenge', challenge):
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

        if request.user.has_perm('update_writeup', writeup):
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

        if request.user.has_perm('create_writeup', challenge):
            writeup = Writeup.objects.create(user=user, challenge=challenge, markdown=request.POST["markdown"])
            writeup.save()

            return redirect(reverse("ctf_framework:writeup#show", args=[writeup.id]))
        else:
            return HttpResponseForbidden("You must solve the challenge first")
