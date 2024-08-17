from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpRequest
from django.views.generic import ListView
from django.core.paginator import Paginator

from blog.forms import EmailPostForm, CommentForm
from blog.models import Post, Comment


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
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


def post_share(request: HttpRequest, post_id: int):
    post: Post = get_object_or_404(Post.published, id=post_id)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
            send_mail(subject, message, from_email=None, recipient_list=[cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


@require_POST
def post_comment(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post.published, id=post_id)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment: Comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )
