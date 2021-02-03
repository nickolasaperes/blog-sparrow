from datetime import date

from django.test import TestCase

from blog.core.models import User


class AuthorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='johndoe', bio='Lorem ipsum', birth_date=date.today())

    def test_create(self):
        self.assertTrue(User.objects.exists())

    def test_birth_null(self):
        """Birth_date can be null"""
        self.assertTrue(User._meta.get_field('birth_date').null)

    def test_birth_can_be_blank(self):
        """Birth_date can be blank"""
        self.assertTrue(User._meta.get_field('birth_date').blank)

    def test_profile_null(self):
        """Profile picture can be null"""
        self.assertTrue(User._meta.get_field('profile').null)

    def test_profile_can_be_blank(self):
        self.assertTrue(User._meta.get_field('profile').blank)
