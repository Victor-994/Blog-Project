from os import name
from django import forms
from django import fields, Model
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
    widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    pass