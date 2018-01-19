from django.db import models
from django.contrib.auth.models import User
from django_slack_oauth.models import SlackUser
from django.core.exceptions import ObjectDoesNotExist


class CTFSlackUser(SlackUser):
    """
    Extending the django oauth SlackUser to support display names
    """
    display_name = models.CharField(max_length=100)


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

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    flag = models.CharField(max_length=100)
    point_value = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    category = models.ForeignKey(ChallengeCategory, on_delete=models.PROTECT)

    def __str__(self):
        return "{} | {} | {}".format(self.category, self.point_value, self.name)


class UserProfile(models.Model):
    """
    Used for storing all user profile information and statistics
    """
    # Django User. Related Name is for retrieving UserProfile in templates (ex: request.user.UserProfile)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="UserProfile")

    # Earned Titles That Can Be Selected by User
    titles = models.ManyToManyField(Title, blank=True)

    # Active Title, Can Be Set To Any (even non-earned) By Admin
    active_title = models.ForeignKey(Title, on_delete=models.PROTECT, related_name="activetitle", blank=True, null=True)

    # Completed Challenges
    challenges = models.ManyToManyField(Challenge, blank=True)

    def __str__(self):
        return self.display_name()

    def get_score(self):
        return sum([c.point_value for c in self.challenges.all()])

    def get_completed_challenges(self):
        """
        Returns a dictionary of {str ChallengeCategory: [completed challenge,],}
        """
        completed_challenges = {}

        for category in ChallengeCategory.objects.all():
            completed_challenges[category.category] = []
            for challenge in self.challenges.filter(category=category):
                completed_challenges[category.category].append(challenge)

        return completed_challenges

    def display_name(self):
        """
        If there's a slack user, return Slack display name. Else, use django username.
        """
        try:
            return CTFSlackUser.objects.get(slacker=self.user).display_name
        except ObjectDoesNotExist:
            return self.user.username











