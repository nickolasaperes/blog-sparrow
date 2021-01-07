from django.test import TestCase
from datetime import datetime
from blog.core.models import Tag


class ModelTagsTest(TestCase):
    def setUp(self):
        self.obj = Tag.objects.create(title='Tag1')

    def test_create(self):
        self.assertTrue(Tag.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Tag1', str(self.obj))
