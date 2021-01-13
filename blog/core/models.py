from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import resolve_url as r

from blog.core.managers import CategoryManager, TagManager


class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CategoryManager()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TagManager()

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    authors = models.ManyToManyField(User)
    thumb = models.ImageField()
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category')
    tags = models.ManyToManyField('Tag')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return r('post-detail', slug=self.slug)
