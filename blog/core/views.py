from django.shortcuts import render


def home(request):
    return render(request, 'core/index.html')


def post_list(request):
    return render(request, 'core/post_list.html')
