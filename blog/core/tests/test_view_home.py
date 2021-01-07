from django.test import TestCase
from blog.core.models import Post
from django.shortcuts import resolve_url as r


class HomeTest(TestCase):
    def setUp(self):
        Post.objects.create(title='Title',
                            slug='title',
                            content='Content')

        obj = Post.objects.create(
            title='Proin gravida nibh vel velit auctor aliquet Aenean sollicitudin auctor.',
            slug='proin-gravida-nibh',
            content='Content',
        )
        obj2 = Post.objects.create(
            title='Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit sed.',
            slug='nemo-enim-ipsam',
            content='Content',
        )
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
                            slug='title-2',
                            content=self.content)

        obj.authors.create(username='john', first_name='John', last_name='Doe')
        obj2.authors.create(username='john2', first_name='John', last_name='Doe')

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
        contents = [
            (1, 'Proin gravida nibh vel velit auctor aliquet Aenean sollicitudin auctor.'),
            (1, 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit sed.'),
            (2, 'John Doe')
        ]

        for count, expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected, count)

    # def test_html_date_format(self):
    #     """Should show created_at datetime formatted as 'Month DD, YYYY'"""
    #     data = datetime.utcnow()
    #     data = data.strftime('%b %d, %Y').upper()
    #     self.assertContains(self.resp, data, 2)

    def test_content_slice(self):
        """Should show only 400 characters in home"""
        self.assertNotContains(self.resp, self.content[400:])

    def test_post_detail_link(self):
        self.assertContains(self.resp, 'href="/post/proin-gravida-nibh"', 3)