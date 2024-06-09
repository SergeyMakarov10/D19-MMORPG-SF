from django_filters import FilterSet, DateFilter
from .models import Post, Comment, User
from django import forms
from django.contrib.auth.models import User

class PostFilter(FilterSet):
    date_created = DateFilter(field_name='post_created_at', widget=forms.DateInput(attrs={'type': 'date'}),
                             lookup_expr='date__gte')
    class Meta:
        model = Post
        fields = {
           # поиск по названию
           'title': ['istartswith'],
           'categories': ['exact'],
        }

class PersonFilter(FilterSet):
    #date_created = DateFilter(field_name='comment_created_at', widget=forms.DateInput(attrs={'type': 'date'}),
                             #lookup_expr='date__gte')
    class Meta:
        model = Comment
        fields = {
           # поиск по названию
           'post',
      }
        labels = {
            'post': ('Объявления'),
        }

    def __init__(self, *args, **kwargs):
        super(PersonFilter, self).__init__(*args, **kwargs)
        self.filters['post'].queryset = Post.objects.filter(post_author=kwargs.get('request'))

