from django.test import TestCase

from blog.core.admin import PostModelAdmin, CategoryModelAdmin, TagModelAdmin, UserModelAdmin
from blog.core.forms import UserCreationAdminForm
from django.contrib.auth.admin import UserAdmin


class UserModelAdminTest(TestCase):
    def test_form(self):
        self.assertEqual(UserModelAdmin.add_form, UserCreationAdminForm)

    def test_fieldsets(self):
        """Should have blog custom columns separated in fieldsets"""
        expected = (
            *UserAdmin.fieldsets,
            (
                'Blog',
                {
                    'fields': (
                        'bio',
                        'birth_date',
                        'profile',
                    )
                }
            )
        )
        self.assertEqual(UserModelAdmin.fieldsets, expected)


class PostModelAdminTest(TestCase):
    def test_prepopulated_fields(self):
        self.assertEqual(PostModelAdmin.prepopulated_fields, {'slug': ('title',)})

    def test_clean_title(self):
        """Should save the first letter of title uppercase"""
        data = dict(title='post post', slug='post', content='content')
        form = PostModelAdmin.form(data)
        form.is_valid()
        self.assertEqual(form.cleaned_data['title'], 'Post post')


class CategoryModelAdminTest(TestCase):
    def test_prepopulated_fields(self):
        self.assertEqual(CategoryModelAdmin.prepopulated_fields, {'slug': ('title',)})

    def test_clean_title(self):
        """Should save the first letter of title uppercase"""
        data = dict(title='category category', slug='category-category')
        form = CategoryModelAdmin.form(data)
        form.is_valid()
        self.assertEqual(form.cleaned_data['title'], 'Category category')


class SlugModelAdminTest(TestCase):
    def test_prepopulated_fields(self):
        self.assertEqual(TagModelAdmin.prepopulated_fields, {'slug': ('title',)})

    def test_clean_title(self):
        """Should save the first letter of title uppercase"""
        data = dict(title='tag tag', slug='tag-tag')
        form = TagModelAdmin.form(data)
        form.is_valid()
        self.assertEqual(form.cleaned_data['title'], 'Tag tag')
