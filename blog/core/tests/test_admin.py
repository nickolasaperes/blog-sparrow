from django.test import TestCase
from blog.core.admin import PostModelAdmin


class PostModelAdminTest(TestCase):
    def test_prepopulated_fields(self):
        self.assertEqual(PostModelAdmin.prepopulated_fields, {'slug': ('title',)})
