from __future__ import division
from django.db import models
from django.contrib.auth.models import User
import math

class Title(models.Model):
    """Titles that can be awarded to users."""

    title = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    CTF challenge categories that can be dynamically added.
    Objects cannot be deleted if a challenge object references them.
    """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class Challenge(models.Model):
    """CTF challenges"""

    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    flag = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    connection_info = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "{} | {} | {}".format(self.category, self.point_value, self.name)

    def first_blood(self):
        """Returns the first user who has solved the challenge."""

        return self.challengesolve_set.all().order_by('solve_time')[0].user or "None"

    def get_total_solves(self):
        return len(self.challengesolve_set.all())

    @property
    def point_value(self):
        challenge_max = 500.0
        challenge_min = 50.0
        decay = 30.0
        value = (
                    (
                        (challenge_min - challenge_max)/(decay**2)
                    ) * (self.get_total_solves()**2)
                ) + challenge_max

        value = math.ceil(value)
        return max(int(value), int(challenge_min))


class UserProfile(models.Model):
    """Used for storing all user profile information and statistics."""

    # Django User. Related Name is for retrieving UserProfile in templates (ex: request.user.UserProfile)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="UserProfile")

    display_name = models.CharField(max_length=100, default="NOT_AVAILABLE")

    completed_challenges = models.ManyToManyField(Challenge, through="ChallengeSolve")

    earned_titles = models.ManyToManyField(Title, through="TitleGrant")

    # Active Title, Can Be Set To Any (even non-earned) By Admin
    active_title = models.ForeignKey(Title, on_delete=models.PROTECT, related_name="activetitle", blank=True, null=True)

    # Registration Time
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    # Used for sorting the scoreboard
    last_solve_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    @property
    def is_staff(self):
        return self.user.is_staff

    def __str__(self):
        return self.display_name

    def get_score(self):
        return sum([c.point_value for c in self.completed_challenges.all()])

    def get_completed_challenges(self):
        """Returns a dictionary of {str Category: [completed challenge,],}."""

        completed_challenges = {}

        for challenge in self.completed_challenges.all():
            tmp = completed_challenges.get(challenge.category, [])
            tmp.append(challenge)
            completed_challenges[challenge.category] = tmp
        return completed_challenges


class ChallengeSolve(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    solve_time = models.DateTimeField(auto_now_add=True, blank=True)


class TitleGrant(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    grant_time = models.DateTimeField(auto_now_add=True, blank=True)


class Writeup(models.Model):
    """CTF writeups"""

    markdown = models.CharField(max_length=5000)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        unique_together = ("user", "challenge")

    def __str__(self):
        return "{} by {}".format(self.challenge, self.user)
