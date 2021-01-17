from datetime import datetime

from django.shortcuts import resolve_url as r
from django.test import TestCase

from blog.core.models import Post

from blog.core.managers import PostManager


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


class TestPostManager(TestCase):
    def setUp(self):
        self.previous = Post.objects.create(title='Title2',
                                            slug='title2',
                                            content='Content')

        self.post = Post.objects.create(title='Title',
                                        slug='title',
                                        content='Content')

        self.next = Post.objects.create(title='Title4',
                                        slug='title4',
                                        content='Content')

        self.post2 = Post.objects.create(title='Title3',
                                         slug='title3',
                                         content='Content')

    def test_manager(self):
        self.assertIsInstance(Post.objects, PostManager)

    def test_previous(self):
        self.assertEqual(self.previous, Post.objects.previous(self.post))

    def test_next(self):
        self.assertEqual(self.next, Post.objects.next(self.post))

    def test_has_no_previous(self):
        self.assertEqual(None, Post.objects.previous(self.previous))

    def test_has_no_next(self):
        self.assertEqual(None, Post.objects.next(self.post2))
