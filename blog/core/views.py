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

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories, tags = get_sidebar_categories_and_tags()
    return render(request, 'core/post_list.html', {'page_obj': page_obj,  'categories': categories, 'tags': tags})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    categories, tags = get_sidebar_categories_and_tags()

    previous = Post.objects.previous(post)
    next_ = Post.objects.next(post)

    return render(request, 'core/post_detail.html', {'post': post, 'categories': categories, 'tags': tags,
                                                     'previous': previous, 'next': next_})


def get_sidebar_categories_and_tags():
    return Category.objects.top_eight(), Tag.objects.top_five()
