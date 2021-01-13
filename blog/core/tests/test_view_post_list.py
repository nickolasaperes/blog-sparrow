from django.shortcuts import resolve_url as r
from django.test import TestCase


class BlogPostListTest(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('blog'))

    def test_get(self):
        """GET /blog should return status code 200"""
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/post_list.html')

    def test_home_link(self):
        self.assertContains(self.resp, 'href="/"')

    def test_context(self):
        self.assertIn('page_obj', self.resp.context)

    def test_quantity_page(self):
        """Should has 3 posts per page"""
        self.assertEqual(self.resp.context['page_obj'].paginator.per_page, 3)

    def test_get_page(self):
        pass