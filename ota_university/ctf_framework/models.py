from django.db import models
from django.contrib.auth.models import User


class Title(models.Model):
    """
    Awardable User Titles
    """
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class ChallengeCategory(models.Model):
    """
    CTF Challenge Categories that can be dynamically added
    Objects cannot be deleted if a Challenge references them
    """

    class Meta:
        # For Displaying in Admin Panel
        verbose_name = "Challenge Categorie"

    category = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.category


class Challenge(models.Model):
    """
    CTF Challenges
    """

    challenge_name = models.CharField(max_length=100)
    challenge_description = models.CharField(max_length=1000)
    flag = models.CharField(max_length=100)
    point_value = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    category = models.ForeignKey(ChallengeCategory, on_delete=models.PROTECT)

    def __str__(self):
        return "{} | {} | {}".format(self.category, self.point_value, self.challenge_name)


class UserProfile(models.Model):
    """
    Used for storing all user profile information and statistics
    """
    # Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Earned Titles That Can Be Selected by User
    titles = models.ManyToManyField(Title, blank=True)

    # Active Title, Can Be Set To Any (even non-earned) By Admin
    active_title = models.ForeignKey(Title, on_delete=models.PROTECT, related_name="activetitle", blank=True)

    # Completed Challenges
    challenges = models.ManyToManyField(Challenge)

    def __str__(self):
        return self.user.username

    def get_score(self):
        return sum([c.point_value for c in self.challenges.all()])









