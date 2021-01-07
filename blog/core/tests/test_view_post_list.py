from django.test import TestCase
from django.shortcuts import resolve_url as r


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
