from django.db import models
from django.db.models import Count


class CategoryManager(models.Manager):
    def top_eight(self):
        return self.annotate(post_count=Count("post")).order_by("-post_count")[:8]


class TagManager(models.Manager):
    def top_five(self):
        return self.annotate(post_count=Count("post")).order_by("-post_count")[:5]


class PostManager(models.Manager):
    def previous(self, obj):
        return self.filter(created_at__lt=obj.created_at).first()

    def next(self, obj):
        return self.filter(created_at__gt=obj.created_at).order_by("created_at").first()
