from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from .resources import CATEGORY_CHOICES


class User(AbstractUser):
    code = models.CharField(max_length=15, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=17, choices=CATEGORY_CHOICES)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.get_name_display()


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    post_created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    post_updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='Цена', blank=True, null=True)
    content = RichTextUploadingField()

    def __str__(self):
        return f'{self.title} : {self.post_author}'

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['post_created_at']

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name="Автор")
    content = models.TextField(verbose_name="Описание")
    comment_created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, verbose_name="Статус")

    def __str__(self):
        return f'{self.comment_author} : {self.content[:20]}'

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
        ordering = ['comment_created_at']

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.pk})