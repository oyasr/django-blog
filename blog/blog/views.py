from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from blog.models import Post
from django.http import HttpRequest
from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 1
    template_name = "blog/post/list.html"


def post_list(request: HttpRequest):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request: HttpRequest, year: int, month: int, day: int, slug: str):
    post = get_object_or_404(
        Post.published,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})
