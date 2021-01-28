from django.contrib import admin
from blog.core.models import Post, Category, Tag
from blog.core.forms import PostAdminForm, CategoryAdminForm, TagAdminForm


class PostModelAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {'slug': ('title',)}


class CategoryModelAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    prepopulated_fields = {'slug': ('title',)}


class TagModelAdmin(admin.ModelAdmin):
    form = TagAdminForm
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Tag, TagModelAdmin)
