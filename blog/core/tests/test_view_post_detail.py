import os
from datetime import datetime

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import resolve_url as r
from django.test import TestCase

from blog.core.models import Post, Category


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

        self.profile = SimpleUploadedFile(name='author-img.png',
                                          content=open('blog/core/static/images/author-img.png', 'rb').read(),
                                          content_type='image/jpeg')

        self.author = self.post.authors.create(username='john', first_name='John', last_name='Doe', bio='Web Developer',
                                               profile=self.profile)
        self.category = self.post.categories.create(title='Programming 2', slug='programming')
        t = self.post.tags.create(title='Tag1', slug='tag1')
        t2 = self.post.tags.create(title='Tag2', slug='tag2')

        self.categories = [
            self.category,
            Category.objects.create(title='Category2', slug='category2'),
        ]

        self.tags = [
            t,
            t2,
        ]

        self.resp = self.client.get(r('post-detail', slug='title'))

    def tearDown(self):
        os.remove(settings.MEDIA_ROOT + '/' + str(self.author.profile))

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
            'Programming 2',
            date.lower(),
            'Web Developer',
        ]

        for expected in contents:
            with self.subTest():
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

    def test_categories_link(self):
        for category in self.categories:
            with self.subTest():
                self.assertContains(self.resp, category.get_absolute_url())

    def test_category_post_link(self):
        """Should have a link for each category in post"""
        self.assertContains(self.resp, self.category.get_absolute_url(), 2)

    def test_tags_links(self):
        """Should have a link for each tag in post"""
        for tag in self.tags:
            with self.subTest():
                self.assertContains(self.resp, tag.get_absolute_url(), 2)

    def test_author_profile(self):
        """Should exist author profile picture"""
        author = self.post.authors.all()[0]
        expected = author.profile.url
        self.assertContains(self.resp, expected)


class PostNotFoundTest(TestCase):
    def test_not_found(self):
        """Should return 404 when raises post DoesNotExist"""
        resp = self.client.get(r('post-detail', slug='not-found'))
        self.assertEqual(resp.status_code, 404)
