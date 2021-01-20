from datetime import datetime

from django.shortcuts import resolve_url as r
from django.test import TestCase

from blog.core.models import Post, Category, Tag


class PostDetailTest(TestCase):
    def setUp(self):
        self.previous = Post.objects.create(title='Title2',
                                            slug='title2',
                                            content='content')

        self.post = Post.objects.create(title='Title',
                                        slug='title',
                                        content='content')

        self.next = Post.objects.create(title='Title3',
                                        slug='title3',
                                        content='content')

        self.post.authors.create(username='john', first_name='John', last_name='Doe')
        c = self.post.categories.create(title='Category1')
        t = self.post.tags.create(title='Tag1')
        t2 = self.post.tags.create(title='Tag2')

        self.categories = [
            c,
            Category.objects.create(title='Category2'),
            Category.objects.create(title='Category3'),
            Category.objects.create(title='Category4'),
            Category.objects.create(title='Category5'),
            Category.objects.create(title='Category6'),
            Category.objects.create(title='Category7'),
            Category.objects.create(title='Category8'),
        ]

        self.tags = [
            t,
            t2,
            Tag.objects.create(title='Tag3'),
            Tag.objects.create(title='Tag4'),
            Tag.objects.create(title='Tag5'),
        ]

        self.resp = self.client.get(r('post-detail', slug='title'))

    def test_get(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/post_detail.html')

    def test_context(self):
        keys = ['post', 'categories', 'tags', 'previous', 'next']
        for expected in keys:
            self.assertIn(expected, self.resp.context)

    def test_html(self):
        date = datetime.utcnow()
        date = date.strftime('%b %d, %Y')
        contents = [
            'Title',
            'content',
            'John Doe',
            'Category1',
            date.lower(),
        ]

        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_tags(self):
        expected = ', '.join(map(lambda x: str(x), self.post.tags.all()))
        self.assertContains(self.resp, expected)

    def test_sidebar_categories(self):
        """Should show top 8 categories(categories with more posts) in view"""
        for expected in self.categories:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_sidebar_tags(self):
        """Should show top 5 tags"""
        for expected in self.tags:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_previous_post(self):
        self.assertContains(self.resp, str(self.previous))

    def test_next_post(self):
        self.assertContains(self.resp, str(self.next))

    def test_search_form(self):
        """Should have a form with a search field and action to /blog"""
        self.assertContains(self.resp, 'action="/blog"')


class PostNotFoundTest(TestCase):
    def test_not_found(self):
        """Should return 404 when raises post DoesNotExist"""
        resp = self.client.get(r('post-detail', slug='not-found'))
        self.assertEqual(resp.status_code, 404)
