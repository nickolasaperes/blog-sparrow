from django.test import TestCase
from blog.core.admin import PostModelAdmin, CategoryModelAdmin, TagModelAdmin


class PostModelAdminTest(TestCase):
    def test_prepopulated_fields(self):
        self.assertEqual(PostModelAdmin.prepopulated_fields, {'slug': ('title',)})


class CategoryModelAdminTest(TestCase):
    def test_prepopulated_fields(self):
        self.assertEqual(CategoryModelAdmin.prepopulated_fields, {'slug': ('title',)})


class SlugModelAdminTest(TestCase):
    def test_prepopulated_fiels(self):
        self.assertEqual(TagModelAdmin.prepopulated_fields, {'slug': ('title',)})
