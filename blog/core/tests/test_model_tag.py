from datetime import datetime

from django.shortcuts import resolve_url as r
from django.test import TestCase

from blog.core.managers import TagManager
from blog.core.models import Tag, Post


class ModelTagsTest(TestCase):
    def setUp(self):
        self.obj = Tag.objects.create(title='Tag1', slug='tag1')

    def test_create(self):
        self.assertTrue(Tag.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Tag1', str(self.obj))

    def test_get_absolute_url(self):
        self.assertEqual(self.obj.get_absolute_url(), r('posts-by-tag', self.obj.slug))


class TagManagerTest(TestCase):
    def test_manager(self):
        self.assertIsInstance(Tag.objects, TagManager)

    def test_top_five(self):
        """Should return a queryset with top 5 tags(tags with more posts associated with)"""
        first_tag = Tag.objects.create(title='First')
        tags = [
            Tag.objects.create(title='Tag1'),
            Tag.objects.create(title='Tag2'),
            Tag.objects.create(title='Tag3'),
            Tag.objects.create(title='Tag4'),
            Tag.objects.create(title='Tag5'),
        ]

        post1 = Post.objects.create(title='Title',
                                    slug='slug',
                                    content='Content')

        post2 = Post.objects.create(title='Title',
                                    slug='slug2',
                                    content='Content')

        post1.tags.set(tags)
        post1.tags.add(first_tag)
        post2.tags.add(first_tag)

        expected = map(lambda x: str(x), [first_tag, *tags[:4]])
        qs = Tag.objects.top_five()
        self.assertQuerysetEqual(qs, expected, lambda x: x.title)

