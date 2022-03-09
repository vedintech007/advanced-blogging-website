from django.urls import path
from .views import *
# from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/',post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', post_share, name="post_share"),
    
    path('new/blog/post/', new_blog_post, name="new_blog"),
    path('blog/posts/', user_blogs, name="user_blogs"),
    path('blog/posts/details/<str:pk>/', user_blog_detail, name="user_blog_detail"),
]
