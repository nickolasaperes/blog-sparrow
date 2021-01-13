from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from blog.core.models import Post, Category, Tag


def home(request):
    posts = Post.objects.all()[:3]
    return render(request, 'core/index.html', {'posts': posts})


def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/post_list.html', {'page_obj': page_obj})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    categories = Category.objects.top_eight()
    tags = Tag.objects.top_five()
    return render(request, 'core/post_detail.html', {'post': post, 'categories': categories, 'tags': tags})
