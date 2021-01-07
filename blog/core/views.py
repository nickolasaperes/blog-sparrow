from django.shortcuts import render, get_object_or_404
from blog.core.models import Post


def home(request):
    posts = Post.objects.all().order_by('-created_at')[:3]
    return render(request, 'core/index.html', {'posts': posts})


def post_list(request):
    return render(request, 'core/post_list.html')


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'core/post_detail.html', {'post': post})
