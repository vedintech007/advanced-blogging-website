from django.urls import path

from .views import *

# from .feeds import LatestPostFeed

app_name = 'blog'

urlpatterns = [
    path('', post_list, name='post_list'),
    path('tag/<slug:tag_slug>/',post_list, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('blog/posts/update/<str:pk>/', update_post, name="post_update"),
    path('blog/posts/delete/<str:pk>/', delete_post, name="post_delete"),
    path('<int:post_id>/share/', post_share, name="post_share"),
    
    path('new/blog/post/', new_blog_post, name="new_blog"),
    path('blog/posts/', user_blogs, name="user_blogs"),
    path('blog/posts/details/<str:pk>/', user_blog_detail, name="user_blog_detail"),
    
    path('pending/blog/posts/', user_pending_blogs, name="pending_blogs"),
    path('rejected/blog/posts/', user_rejected_blogs, name="rejected_blogs"),
    
    
]
