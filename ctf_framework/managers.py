from django.db import models

class CategoryQuerySet(models.QuerySet):

    def main_categories(self):
        return self.filter(parent_id=None)
