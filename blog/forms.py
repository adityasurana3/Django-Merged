
from pyexpat import model
from django import forms
from django.forms import fields
from .models import Post, Comments, MyUser, Category
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 
                'text', 
                'thumbnail_image',
                'featured_image', 
                'category', 'tag')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('name', 'email', 'comment')

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',) 

class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    # fields =
    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email_id', 'phone_no',
                  'image', 'city', 'state', 'country', 'about', 'company', 'designation',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username','first_name', 'last_name', 'email_id', 'phone_no',
                  'image', 'city', 'state', 'country')
