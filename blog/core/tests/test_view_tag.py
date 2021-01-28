from django.test import TestCase

from blog.core.models import Post


class ViewTagTest(TestCase):
    def setUp(self):
        Post.objects.create(title='Post', slug='post', content='tutorial-django')
        self.post = Post.objects.create(title='Tutorial', slug='tutorial', content='Tutorial Django')
        self.tag = self.post.tags.create(title='Programming', slug='programming')
        self.resp = self.client.get('/tag/programming')

    def test_get(self):
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/post_list.html')

    def test_context(self):
        keys = ['page_obj', 'categories', 'tags']
        for expected in keys:
            with self.subTest():
                self.assertIn(expected, self.resp.context)

    def test_posts(self):
        self.assertQuerysetEqual(self.resp.context['page_obj'], [self.post.title], lambda x: x.title)

    def test_html(self):
        contents = (
            (1, 'Tutorial Django'),
            (2, 'Tutorial'),
            (1, 'tutorial'),
            (1, 'Programming'),
            # (1, 'programming')
        )
        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected, count)


class ViewTagNotFoundTest(TestCase):
    def test_not_found(self):
        resp = self.client.get('/tag/design')
        self.assertEqual(resp.status_code, 404)
