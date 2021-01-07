from django.test import TestCase
from datetime import datetime
from blog.core.models import Category


class ModelCategoriesTest(TestCase):
    def setUp(self):
        self.obj = Category.objects.create(title='Category1')

    def test_create(self):
        self.assertTrue(Category.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Category1', str(self.obj))
