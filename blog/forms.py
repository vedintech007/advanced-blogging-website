from django import forms
from .models import Comment, Post


class BlogPostForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Post
        fields = ('cover_image', 'title', 'body', 'tags')


class EmailPostForm(forms.Form):
    name = forms.CharField(
        max_length=25, 
        label="Your Full Name",
        widget=forms.TextInput()
        )
    email = forms.EmailField(label="Your Email")
    to = forms.EmailField(label="Reciever Email")
    comments = forms.CharField(
        required=False,
        label="Your Comment",
        widget=forms.Textarea(attrs={
            'placeholder': 'Please add some comments in the section so the reciever can know what this post is about out of the box. \n\nEg. Hi Mark this post talks about programming in dept, please check it out.'
        })
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        

class SearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for blogs...',
                'class': 'form-control my-1 p-3 fs-4',
                'type': 'search',
                'list': 'suggestions',
            }
        )
    )