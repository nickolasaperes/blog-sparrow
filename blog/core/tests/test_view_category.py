from django.test import TestCase

from blog.core.models import Tag, Post


class ViewCategoryTest(TestCase):
    def setUp(self):
        Tag.objects.create(title='Web Development', slug='web-development')
        Post.objects.create(title='Post2',
                            content='Content2')
        self.post = Post.objects.create(title='Post',
                                        slug='post',
                                        content='Programming Tutorial')
        self.post.categories.create(title='Design and Digital Art', slug='design')

        self.resp = self.client.get('/category/design')

    def test_get(self):
        """GET /category/<slug> should return status code 200"""
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/post_list.html')

    def test_context(self):
        keys = ['page_obj', 'categories', 'tags']
        for expected in keys:
            with self.subTest():
                self.assertIn(expected, self.resp.context)

    def test_posts(self):
        self.assertQuerysetEqual(self.resp.context['page_obj'], ['Post'], lambda x: x.title)

    def test_html(self):
        contents = (
            (1, 'Web Development'),
            (2, 'Design and Digital Art'),
            (1, 'Post'),
            (1, 'Programming Tutorial'),
        )
        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected, count)


class ViewCategoryTestNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get('/category/not-found')
        self.assertEqual(resp.status_code, 404)
