from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.http import HttpRequest


def post_list(request: HttpRequest):
    posts = Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request: HttpRequest, id: int):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, "blog/post/detail.html", {"post": post})
