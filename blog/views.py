from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post

# Create your views here.


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 12) # number of posts to show per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver the last page of the results
        posts = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'posts': posts,
        'object_list': object_list.count()
    }

    return render(request, 'blog/post/index.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                            publish__year=year, publish__month=month, publish__day=day)

    context = {
        'post': post
    }

    return render(request, 'blog/post/detail.html', context)
