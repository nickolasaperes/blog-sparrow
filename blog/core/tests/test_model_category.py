from datetime import datetime

from django.test import TestCase

from blog.core.managers import CategoryManager
from blog.core.models import Category, Post


class ModelCategoriesTest(TestCase):
    def setUp(self):
        self.obj = Category.objects.create(title='Category1')

    def test_create(self):
        self.assertTrue(Category.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Category1', str(self.obj))


class CategoryManagerTest(TestCase):
    def setUp(self):
        self.first_category = Category.objects.create(title='First')
        self.categories = [
            Category.objects.create(title='Designs'),
            Category.objects.create(title='Internet'),
            Category.objects.create(title='Typography'),
            Category.objects.create(title='Photography'),
            Category.objects.create(title='Web Development'),
            Category.objects.create(title='Projects'),
            Category.objects.create(title='Other Stuff'),
            Category.objects.create(title='Animation'),
            Category.objects.create(title='Not Show')
        ]

        post1 = Post.objects.create(title='Title',
                                    slug='slug',
                                    content='Content')

        post2 = Post.objects.create(title='Title',
                                    slug='slug2',
                                    content='Content')

        post1.categories.set(self.categories)
        post1.categories.add(self.first_category)
        post2.categories.add(self.first_category)

    def test_manager(self):
        self.assertIsInstance(Category.objects, CategoryManager)

    def test_top_eight(self):
        """Should return the 8 categories that has more post associated with"""
        qs = Category.objects.top_eight()
        expected = [self.first_category, *self.categories[:7]]
        expected = map(lambda x: str(x), expected)
        self.assertQuerysetEqual(qs, expected, lambda o: o.title)
