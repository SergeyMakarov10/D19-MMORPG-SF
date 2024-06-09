from django.contrib.auth.models import User
from .models import Post, Comment, Category
from django import forms
from django.contrib import admin
from django.forms import ModelForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.conf import settings
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    #description = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [ 'title', 'content', 'categories', 'price']
        widgets = {
            'text': CKEditorUploadingWidget(),  # поле для загрузки файлов при помощи ckeditor
        }


class CommentForm(forms.ModelForm):
    #description = forms.CharField(min_length=20)

    class Meta:
        model = Comment
        fields = ['post', 'content']
        labels = {
            'post': ('Объявления'),
            'content': ('Текст')
        }