import markdown
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post
# Create your views here.

def index(request):
    # return HttpResponse('welcome to blog') 
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',  # 语法高亮
                                      'markdown.extensions.toc',   # 允许自动生成目录
                                  ])
    return render(request, 'blog/detail.html', context={'post': post})