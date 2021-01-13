from django.db import models
from django.db.models import Count


class CategoryManager(models.Manager):
    def top_eight(self):
        return self.annotate(post_count=Count('post')).order_by('-post_count')[:8]


class TagManager(models.Manager):
    def top_five(self):
        return self.annotate(post_count=Count('post')).order_by('-post_count')[:5]
