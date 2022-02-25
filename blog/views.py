from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render, redirect
import random

from .forms import *
from .models import *


def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 12)  # number of posts to show per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver the last page of the results
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

    # list the active comments for this post
    # we use post.comments.filter() bcos we added related_name='comment' to the comments model
    comments = post.comment.filter(active=True)

    new_comment = None

    if request.method == "POST":
        # A comment was posted
        post_url = request.build_absolute_uri(post.get_absolute_url())
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # create comment object but dont save to database yet
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            # we are just updating the already stored data
            new_comment.post = post
            # save the comment to the database
            new_comment.save()
            return redirect(post_url)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }

    return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
    # retrive post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            # store form data in cd variable
            cd = form.cleaned_data
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Hi there, its {cd['name']} here. I want recommend the blog titled {post.title} at {post_url} for you to read.\n\n Read {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'admin@vedintechblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    context = {
        'post': post,
        'form': form,
        'sent': sent
    }

    return render(request, 'blog/post/share.html', context)
