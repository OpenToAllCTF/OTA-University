from django.db import models
from django.contrib.auth.models import User


class Title(models.Model):
    """Titles that can be awarded to users."""

    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class ChallengeCategory(models.Model):
    """
    CTF challenge categories that can be dynamically added.
    Objects cannot be deleted if a challenge object references them.
    """

    category = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.category


class Challenge(models.Model):
    """CTF challenges"""

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    flag = models.CharField(max_length=100)
    point_value = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    category = models.ForeignKey(ChallengeCategory, on_delete=models.PROTECT)
    url = models.CharField(max_length=100)

    def __str__(self):
        return "{} | {} | {}".format(self.category, self.point_value, self.name)


class UserProfile(models.Model):
    """Used for storing all user profile information and statistics."""

    # Django User. Related Name is for retrieving UserProfile in templates (ex: request.user.UserProfile)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="UserProfile")

    # Earned Titles That Can Be Selected by User
    titles = models.ManyToManyField(Title, blank=True)

    # Active Title, Can Be Set To Any (even non-earned) By Admin
    active_title = models.ForeignKey(Title, on_delete=models.PROTECT, related_name="activetitle", blank=True, null=True)

    # Completed Challenges
    completed_challenges = models.ManyToManyField(Challenge, blank=True)

    display_name = models.CharField(max_length=100, default="NOT_AVAILABLE")

    def __str__(self):
        return self.display_name

    def get_score(self):
        return sum([c.point_value for c in self.completed_challenges.all()])

    def get_completed_challenges(self):
        """Returns a dictionary of {str ChallengeCategory: [completed challenge,],}."""

        completed_challenges = {}

        for challenge in self.completed_challenges.all():
            tmp = completed_challenges.get(challenge.category, [])
            tmp.append(challenge)
            completed_challenges[challenge.category] = tmp
        return completed_challenges
