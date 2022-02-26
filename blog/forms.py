from django import forms
from .models import Comment


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