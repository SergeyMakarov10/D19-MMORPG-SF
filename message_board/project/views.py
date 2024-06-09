from django.shortcuts import render
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from .models import Post, Comment, Category
from Board_News.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .filters import PostFilter, PersonFilter
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy



class PostList(LoginRequiredMixin, ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-post_created_at'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/post.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    queryset = Post.objects.all()
    paginate_by = 5

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

class MyPostList(LoginRequiredMixin, ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-post_created_at'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'flatpages/my_post.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'my_posts'
    queryset = Post.objects.all()
    paginate_by = 5


    def get_queryset(self):

        queryset = Post.objects.filter(post_author=self.request.user.pk).order_by('-post_created_at')
        self.filterset = PostFilter(self.request.GET, queryset)
         # Возвращаем из функции отфильтрованный список объявлений пользователя
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
         # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context



class PostDetail(LoginRequiredMixin, DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'flatpages/post_id.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post_id'

class MyPostDetail(LoginRequiredMixin, DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'flatpages/my_post_id.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'my_post_id'


class PostCreate(LoginRequiredMixin,CreateView):
    permission_required = ('post.add_post',)
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'flatpages/post_create.html'

    # добавляем создание поста только от имени текущего пользователя
    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_author = self.request.user
        post.save()
        #send_email_task.delay(post.pk)
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    #fields = [ 'title', 'content', 'post_author', 'categories', 'price']
    template_name = 'flatpages/post_update.html'
    form_class = PostForm
    # добавляем обновление поста, созданного только текущим пользователем
    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        # send_email_task.delay(post.pk)
        return super().form_valid(form)

class PostDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('post.delete_post',)
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('post')



class CommentCreate(LoginRequiredMixin, CreateView):
    permission_required = ('comment.add_comment',)
    # Указываем нашу разработанную форму
    form_class = CommentForm
    # модель товаров
    model = Comment
    # и новый шаблон, в котором используется форма.
    template_name = 'flatpages/comment_create.html'
    context_object_name = 'comments'

    # добавляем создание комментария только от имени текущего пользователя
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.comment_author = self.request.user
        comment.save()
        # send_email_task.delay(post.pk)
        return super().form_valid(form)

class HomePage(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/mainpost.html'
    # def form_valid(self, form):
    #     comment = form.save(commit=False)
    #     comment.save()
    #     #send_email_task.delay(post.pk)
    #     return super().form_valid(form)

class PersonCabinet(LoginRequiredMixin, ListView):
    # Указываем модель, объекты которой мы будем выводить
    #model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-post_created_at'
    template_name = 'flatpages/person_cabinet.html'
    context_object_name = 'person_cabinet'
    queryset = Post.objects.all()
    paginate_by = 5

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = Comment.objects.filter(post__post_author=self.request.user.pk).order_by('-comment_created_at')
        #queryset = Post.objects.filter(post_author=self.request.user.pk).order_by('-post_created_at')
        self.filterset = PersonFilter(self.request.GET, queryset, request=self.request.user.pk)
        # Возвращаем из функции отфильтрованный список товаров
        if self.request.GET:
            return self.filterset.qs
        return Comment.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    # def get_queryset(self):
    #     queryset = Post.objects.filter(post_author=self.request.user.id).order_by('-post_created_at')
    #     return queryset




def comment_accept(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.status = True
    comment.save()
    return redirect(reverse('person_cabinet'))

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect(reverse('person_cabinet'))




class CategoryName(ListView):
    model = Category
    template_name = 'flatpages/category_name.html'
    context_object_name = 'category_name'

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return  render(request, 'flatpages/subscribe.html', {'category': category, 'message': message})

@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы успешно отменили подписку на рассылку новостей категории'
    return  render(request, 'flatpages/unsubscribe.html', {'category': category, 'message': message})
