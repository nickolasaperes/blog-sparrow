from datetime import datetime

from django.shortcuts import resolve_url as r
from django.test import TestCase

from blog.core.models import Post


class PostDetailTest(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title='Title',
                                        slug='title',
                                        content='content')

        self.post.authors.create(username='john', first_name='John', last_name='Doe')
        self.post.categories.create(title='Category')
        self.post.tags.create(title='Django')

        self.resp = self.client.get(r('post-detail', slug='title'))

    def test_get(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/post_detail.html')

    def test_context(self):
        post = self.resp.context['post']
        self.assertIsInstance(post, Post)

    def test_html(self):
        date = datetime.utcnow()
        date = date.strftime('%b %d, %Y')
        contents = [
            'Title',
            'content',
            'John Doe',
            'Category',
            'Django',
            date.lower(),
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)


class PostNotFoundTest(TestCase):
    def test_not_found(self):
        """Should return 404 when raises post DoesNotExist"""
        resp = self.client.get(r('post-detail', slug='not-found'))
        self.assertEqual(resp.status_code, 404)
