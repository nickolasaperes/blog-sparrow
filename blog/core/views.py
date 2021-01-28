from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from blog.core.models import Post, Category, Tag


def home(request):
    posts = Post.objects.all()[:3]
    return render(request, 'core/index.html', {'posts': posts})


def post_list(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(title__icontains=query)
    else:
        posts = Post.objects.all()

    page_obj = _post_list_paginator(request, posts)

    categories, tags = _get_sidebar_categories_and_tags()
    return render(request, 'core/post_list.html', {'page_obj': page_obj,  'categories': categories, 'tags': tags})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    categories, tags = _get_sidebar_categories_and_tags()

    previous = Post.objects.previous(post)
    next_ = Post.objects.next(post)

    return render(request, 'core/post_detail.html', {'post': post, 'categories': categories, 'tags': tags,
                                                     'previous': previous, 'next': next_})


def posts_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.post_set.all()
    page_obj = _post_list_paginator(request, posts)

    categories, tags = _get_sidebar_categories_and_tags()
    return render(request, 'core/post_list.html', {'page_obj': page_obj, 'categories': categories, 'tags': tags})


def posts_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = tag.post_set.all()
    page_obj = _post_list_paginator(request, posts)

    categories, tags = _get_sidebar_categories_and_tags()
    return render(request, 'core/post_list.html', {'page_obj': page_obj, 'categories': categories, 'tags': tags})


def _get_sidebar_categories_and_tags():
    return Category.objects.top_eight(), Tag.objects.top_five()


def _post_list_paginator(request, posts):
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
