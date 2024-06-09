from django.contrib import admin
from .models import User
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import *

class PostAdminForm(forms.ModelForm):
    text = forms.CharField(label='Текст', widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)

