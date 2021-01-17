from django.shortcuts import resolve_url as r
from django.test import TestCase
from blog.core.models import Post, Tag, Category

from django.core.paginator import EmptyPage


class BlogPostListTest(TestCase):
    def setUp(self):
        Post.objects.create(title='Title',
                            slug='title',
                            content='Content')
        Post.objects.create(title='Title',
                            slug='title2',
                            content='Content')
        Post.objects.create(title='Title',
                            slug='title2',
                            content='Content')
        Post.objects.create(title='Title3',
                            slug='title3',
                            content='Content')

        self.categories = [
            Category.objects.create(title='Category1'),
            Category.objects.create(title='Category2'),
            Category.objects.create(title='Category3'),
            Category.objects.create(title='Category4'),
            Category.objects.create(title='Category5'),
            Category.objects.create(title='Category6'),
            Category.objects.create(title='Category7'),
            Category.objects.create(title='Category8'),
        ]

        self.tags = [
            Tag.objects.create(title='Tag1'),
            Tag.objects.create(title='Tag2'),
            Tag.objects.create(title='Tag3'),
            Tag.objects.create(title='Tag4'),
            Tag.objects.create(title='Tag5'),
        ]

        self.resp = self.client.get(r('blog'))

    def test_get(self):
        """GET /blog should return status code 200"""
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/post_list.html')

    def test_home_link(self):
        self.assertContains(self.resp, 'href="/"')

    def test_context(self):
        keys = ['categories', 'page_obj', 'tags']
        for key in keys:
            with self.subTest():
                self.assertIn(key, self.resp.context)

    def test_quantity_page(self):
        """Should has 3 posts per page"""
        self.assertEqual(self.resp.context['page_obj'].paginator.per_page, 3)

    def test_get_page(self):
        """If get page 2 should show only the first element created, post with title 'Title'"""
        post = list(self.resp.context['page_obj'].paginator.page(2))[0]
        self.assertEqual(str(post), 'Title')

    def test_get_page_exceeding(self):
        self.assertRaises(EmptyPage, self.resp.context['page_obj'].paginator.page, 3)

    def test_sidebar_categories(self):
        for category in self.categories:
            with self.subTest():
                self.assertContains(self.resp, str(category))

    def test_sidebar_tags(self):
        for tag in self.tags:
            with self.subTest():
                self.assertContains(self.resp, str(tag))
