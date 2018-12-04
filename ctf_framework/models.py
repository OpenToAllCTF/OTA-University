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

    @property
    def challenges(self):
        return self.challenge_set.all()

    def __str__(self):
        return self.name


class Challenge(models.Model):
    """Represents a CTF challenge"""

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

    @property
    def number_of_solves(self):
        return self.solve_set.count

    @property
    def point_value(self):
        challenge_max = 500.0
        challenge_min = 50.0
        decay = 30.0
        value = (
                    (
                        (challenge_min - challenge_max) / (decay ** 2)
                    ) * (self.number_of_solves() ** 2)
                ) + challenge_max

        value = math.ceil(value)
        return max(int(value), int(challenge_min))

    @property
    def first_blood(self):
        first_solve = self.solve_set.first()

        if first_solve:
            return first_solve.user

        return None


class UserProfile(models.Model):
    """Used for storing all user profile information and statistics."""

    # Django User. Related Name is for retrieving UserProfile in templates (ex: request.user.UserProfile)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="UserProfile")

    display_name = models.CharField(max_length=100, default="NOT_AVAILABLE")

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

    @property
    def score(self):
        return sum([solve.challenge.point_value for solve in self.solves])

    @property
    def solves(self):
        return self.solve_set.all()

    @property
    def titles(self):
        return self.earned_titles.all()

    @property
    def missing_titles(self):
        return Title.objects.filter().exclude(id__in=self.titles)

    def __str__(self):
        return self.display_name


class Solve(models.Model):
    """Represents a challenge solved by a user at a specific time."""

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ('date', )


class TitleGrant(models.Model):
    """Represents a title granted to a user at a specific time."""

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
