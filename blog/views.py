from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from taggit.models import Tag


from .forms import *
from .models import *


@login_required
def new_blog_post(request):
    form = BlogPostForm()
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES,)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            title = obj.title
            obj.save()
            messages.success(
                request, f'Blog <b>"{title}"</b> Created successfully!')
            return redirect('blog:user_blogs')

    context = {
        'form': form,
    }

    return render(request, 'blog/post/new_blog.html', context)


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    featured_posts = Post.published.filter(featured=True).order_by('-created')
    tag = None
    form = SearchForm()
    query = None
    blog_filtered = False

    # Blog Search Filter logic
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            if query == '' or query == None:
                return redirect('blog:post_list')
            else:
                object_list = Post.published.annotate(
                    search=SearchVector('title', 'body', 'author'),
                ).filter(search=query)
                blog_filtered = True

    # Tag Filter logic
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # Pagination logic
    paginator = Paginator(object_list, 9)  # number of posts to show per page
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
        'post_count': object_list.count(),
        'tag': tag,
        'form': form,
        'query': query,
        'blog_filtered': blog_filtered,
        
        'featured_posts': featured_posts,
        'featured_posts_count': featured_posts.count(),
    }

    return render(request, 'blog/post/index.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                            publish__year=year, publish__month=month, publish__day=day)
    posts = Post.published.all()[:2]
    form = SearchForm()

    query = None
    blog_filtered = False

    # Blog Search Filter logic
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            if query == '' or query == None:
                return redirect('blog:post_list')
            else:
                object_list = Post.published.annotate(
                    search=SearchVector('title', 'body'),
                ).filter(search=query)
                blog_filtered = True

    # List Similar posts
    post_tag_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')

    # list the active comments for this post
    # we use post.comments.filter() bcos we added related_name='comment' to the comments model
    comments = post.comment.filter(active=True)

	# add comment login
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
            messages.success(request, "New comment added successfully")
            return redirect(post_url)
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'posts': posts,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts,
        'form': form,
        'query': query,
        'blog_filtered': blog_filtered,
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
            subject = f"{cd['name']} recommends {post.title}"
            message = f"""
			Blog Recommended By: {cd['name']}
			
			Blog title: {post.title}
			
			{cd['name']} Comments: {cd['comments']}
						
			Link to Blog: {post_url}
			"""
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


def update_post(request, pk):
    post = Post.objects.get(id=pk)
    post_form = BlogPostUpdateForm(instance=post)

    if request.method == "POST":
        post_form = BlogPostUpdateForm(request.POST, request.FILES, instance=post)

        if post_form.is_valid():
            post_form.save()
            
            messages.success(request, "Blog post updated successfully")
            return redirect('blog:post_list')
        else:
            messages.error(request, "Error updating your profile")
            print(messages)

    context = {
        'post_form': post_form
    }

    return render(request, 'blog/post/blog_update.html', context)


@login_required
def delete_post(request, pk):
    post = Post.objects.get(id=pk)
    title = post.title

    if request.method == "POST":
        messages.success(request, f"Blog post '{title}' deleted successfully")
        post.delete()
        return redirect('blog:post_list')
    else:
        messages.error(request, f"Error deleting blog '{title}'")
        return redirect('blog:post_list')


@login_required
def user_blogs(request):
    object_list = Post.objects.filter(author=request.user).order_by('-created')
    form = SearchForm()
    query = None
    blog_filtered = False

    # Blog Search Filter logic
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            if query == '' or query == None:
                return redirect('blog:user_blogs')
            else:
                object_list = Post.objects.annotate(
                    search=SearchVector('title', 'body', 'status'),
                ).filter(search=query, author=request.user)
                blog_filtered = True

    # Pagination logic
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
        'object_list': object_list.count(),
        'form': form,
        'query': query,
        'blog_filtered': blog_filtered,
    }

    return render(request, 'blog/post/user_blogs.html', context)


@login_required
def user_blog_detail(request, pk):
    post = Post.objects.get(id=pk)
    form = SearchForm()
    query = None
    blog_filtered = False
    posts = Post.published.all()

    # Blog Search Filter logic
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            if query == '' or query == None:
                return redirect('blog:post_list')
            else:
                object_list = Post.published.annotate(
                    search=SearchVector('title', 'body'),
                ).filter(search=query)
                blog_filtered = True

    # List Similar posts
    post_tag_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tag_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-publish')[:5]

    # list the active comments for this post
    # we use post.comments.filter() bcos we added related_name='comment' to the comments model
    comments = post.comment.filter(active=True)

    context = {
        'post': post,
        'posts': posts,
        'comments': comments,
        'similar_posts': similar_posts,
        'form': form,
        'query': query,
        'blog_filtered': blog_filtered,
    }

    return render(request, 'blog/post/user_blog_details.html', context)


@login_required
def user_pending_blogs(request):
    object_list = Post.objects.filter(status='draft').order_by('-created')
    form = SearchForm()
    query = None
    blog_filtered = False

    # Blog Search Filter logic
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            if query == '' or query == None:
                return redirect('blog:user_blogs')
            else:
                object_list = Post.objects.annotate(
                    search=SearchVector('title', 'body', 'status', 'author'),
                ).filter(search=query, status='draft')
                blog_filtered = True

    # Pagination logic
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
        'object_list': object_list.count(),
        'form': form,
        'query': query,
        'blog_filtered': blog_filtered,
    }

    return render(request, 'blog/post/user_pending_blogs.html', context)


@login_required
def user_rejected_blogs(request):
    object_list = Post.objects.filter(status='rejected').order_by('-created')
    form = SearchForm()
    query = None
    blog_filtered = False

    # Blog Search Filter logic
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']

            if query == '' or query == None:
                return redirect('blog:user_blogs')
            else:
                object_list = Post.objects.annotate(
                    search=SearchVector('title', 'body', 'status', 'author'),
                ).filter(search=query, status='rejected')
                blog_filtered = True

    # Pagination logic
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
        'object_list': object_list.count(),
        'form': form,
        'query': query,
        'blog_filtered': blog_filtered,
    }

    return render(request, 'blog/post/user_rejected_blogs.html', context)
