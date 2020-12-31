from django.test import TestCase


class HomeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')

    def test_get(self):
        """GET / should return 200"""
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/index.html')

    def test_blog_link(self):
        self.assertContains(self.resp, 'href="/blog"')
