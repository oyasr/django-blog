from django.urls import path
from blog.views import post_list, post_detail, PostListView


app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path(
        "<int:year>/<int:month>/<int:day>/<slug:slug>/", post_detail, name="post_detail"
    ),
]
