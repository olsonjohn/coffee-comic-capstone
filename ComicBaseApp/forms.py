from django import forms
from ComicBaseApp.models import ComicUser, ComicBook, ComicComment


# Authenication Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


# Authenication Signup Form
class SignUpForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    display_name = forms.CharField(max_length=50)
    bio = forms.CharField(max_length=250)
    email = forms.EmailField(max_length=100)


class CommentForm(forms.ModelForm):
    class Meta:
        model = ComicComment
        fields = ['comment']
    