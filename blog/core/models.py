from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import resolve_url as r

from blog.core.managers import CategoryManager, TagManager, PostManager


class User(AbstractUser):
    bio = models.TextField(max_length=300)
    birth_date = models.DateField(null=True, blank=True)
    profile = models.ImageField(null=True, blank=True)


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CategoryManager()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "{}?category={}".format(r("blog"), self.slug)


class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TagManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return "{}?tag={}".format(r("blog"), self.slug)


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    authors = models.ManyToManyField(User)
    thumb = models.ImageField()
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField("Category")
    tags = models.ManyToManyField("Tag")

    objects = PostManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return r("post-detail", slug=self.slug)
