from datetime import datetime

from django.shortcuts import resolve_url as r
from django.test import TestCase

from blog.core.models import Post


class ModelPostTest(TestCase):
    def setUp(self):
        self.obj = Post.objects.create(title='Title',
                                       slug='title',
                                       content='Content')

    def test_create(self):
        self.assertTrue(Post.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_post_has_many_authors(self):
        self.obj.authors.create(username='Author')
        self.assertEqual(1, self.obj.authors.count())

    def test_post_has_many_categories(self):
        self.obj.categories.create(title='Category1')
        self.assertEqual(1, self.obj.categories.count())

    def test_post_has_many_tags(self):
        self.obj.tags.create(title='Tag1')
        self.assertEqual(1, self.obj.tags.count())

    def test_str(self):
        self.assertEqual('Title', str(self.obj))

    def test_absolute_url(self):
        self.assertEqual(self.obj.get_absolute_url(), r('post-detail', slug='title'))

    def test_ordering(self):
        self.assertEqual(['-created_at'], Post._meta.ordering)
