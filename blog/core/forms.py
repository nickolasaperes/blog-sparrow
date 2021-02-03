from django import forms
from django.contrib.auth.forms import UserCreationForm
from blog.core.models import Post, Category, Tag, User


class UserCreationAdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'


class BaseAdminForm:
    def clean_title(self):
        title = self.cleaned_data['title']
        return title[0].upper() + title[1:]


class PostAdminForm(forms.ModelForm, BaseAdminForm):
    class Meta:
        model = Post
        fields = '__all__'


class CategoryAdminForm(forms.ModelForm, BaseAdminForm):
    class Meta:
        model = Category
        fields = '__all__'


class TagAdminForm(forms.ModelForm, BaseAdminForm):
    class Meta:
        model = Tag
        fields = '__all__'
