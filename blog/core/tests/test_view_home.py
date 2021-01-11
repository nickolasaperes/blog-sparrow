from datetime import datetime

from django.shortcuts import resolve_url as r
from django.test import TestCase

from blog.core.models import Post

from django.contrib.auth.models import User


class HomeTest(TestCase):
    def setUp(self):
        self.content = """
            Proin gravida nibh vel velit auctor aliquet. Aenean sollicitudin, lorem quis bibendum auctor, nisi elit consequat ipsum, nec sagittis sem nibh id elit.
            Duis sed odio sit amet nibh vulputate cursus a sit amet mauris. Morbi accumsan ipsum velit. Nam nec tellus a odio tincidunt auctor a ornare odio.
            Sed non mauris vitae erat consequat auctor eu in elit.
            Proin gravida nibh vel velit auctor aliquet. Aenean sollicitudin, lorem quis bibendum auctor, nisi elit consequat ipsum, nec sagittis sem nibh id elit.
            Duis sed odio sit amet nibh vulputate cursus a sit amet mauris. Morbi accumsan ipsum velit. Duis sed odio sit amet nibh vulputate cursus a sit amet mauris.
            Morbi accumsan ipsum velit. At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate.
            At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium. Proin gravida nibh vel velit auctor aliquet. Aenean sollicitudin, lorem quis bibendum auctor, nisi elit consequat ipsum, nec sagittis sem nibh id elit.
            Duis sed odio sit amet nibh vulputate cursus a sit amet mauris. Morbi accumsan ipsum velit. Duis sed odio sit amet nibh vulputate cursus a sit amet mauris. Morbi accumsan ipsum velit.
        """

        Post.objects.create(title='Title',
                            slug='title4',
                            content=self.content)

        self.obj = Post.objects.create(title='Title',
                                       slug='title',
                                       content='Content')

        self.obj2 = Post.objects.create(title='Title',
                                        slug='title2',
                                        content='Content')

        self.obj3 = Post.objects.create(title='Title',
                                        slug='title3',
                                        content='Content')

        author = User.objects.create(username='john', first_name='John', last_name='Doe')
        self.obj.authors.add(author)
        self.obj2.authors.add(author)
        self.obj3.authors.add(author)

        self.resp = self.client.get(r('home'))

    def test_get(self):
        """GET / should return 200"""
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/index.html')

    def test_blog_link(self):
        self.assertContains(self.resp, 'href="/blog"')

    def test_context(self):
        """Should have a posts list in response context"""
        self.assertIn('posts', self.resp.context)

    def test_posts_len(self):
        """Should return maximum of 3 posts"""
        self.assertEqual(len(self.resp.context['posts']), 3)

    def test_html(self):
        date = datetime.utcnow()
        date = date.strftime('%b %d, %Y')
        date = date.lower()
        contents = [
            (3, 'Title'),
            (3, 'John Doe'),
            (3, date),
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected, count)

    def test_content_slice(self):
        """Should show only 400 characters in home"""
        self.assertNotContains(self.resp, self.content[400:])

    def test_post_detail_link(self):
        contents = [
            r('post-detail', 'title'),
            r('post-detail', 'title2'),
            r('post-detail', 'title3'),
        ]
        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, 'href="{}"'.format(expected))
