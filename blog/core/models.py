from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return self.title
