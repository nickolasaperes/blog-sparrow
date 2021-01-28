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
        obj = Post.objects.create(title='Title3',
                                  slug='title3',
                                  content='Content')

        self.category = obj.categories.create(title='Category1', slug='category1')
        self.categories = [
            self.category,
            Category.objects.create(title='Category2', slug='category2'),
        ]

        self.tags = [
            Tag.objects.create(title='Tag1', slug='tag1'),
            Tag.objects.create(title='Tag2', slug='tag2'),
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

    def test_categories_link(self):
        for category in self.categories:
            with self.subTest():
                self.assertContains(self.resp, category.get_absolute_url())

    def test_link_category_of_post(self):
        """Should have a link for each category in post"""
        self.assertContains(self.resp, self.category.get_absolute_url(), 2)

    def test_tags_links(self):
        """Should have link of tags in sidebar"""
        for tag in self.tags:
            with self.subTest():
                self.assertContains(self.resp, tag.get_absolute_url())


class SearchTest(TestCase):
    def setUp(self):
        Post.objects.create(title='Title',
                            slug='title',
                            content='Content')
        Post.objects.create(title='Title2',
                            slug='title2',
                            content='Content')

        self.resp = self.client.get(r('blog'), {'q': 'Title2'})

    def test_search(self):
        self.assertQuerysetEqual(self.resp.context['page_obj'], ['Title2'], lambda x: x.title)

    def test_persistent_query(self):
        self.assertQuerysetEqual(self.resp.context['page_obj'].paginator.get_page(2), ['Title2'], lambda x: x.title)
