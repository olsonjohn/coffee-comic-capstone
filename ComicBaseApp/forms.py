from django import forms
from ComicBaseApp.models import ComicUser, ComicBook, ComicComment


# Authenication Signup Form



# Authenication Login Form




class CommentForm(forms.ModelForm):
    class Meta:
        model = ComicComment
        fields = ['comment']
    