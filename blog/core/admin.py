from django.contrib import admin
from blog.core.models import Post, Category, Tag


class PostModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Tag)
