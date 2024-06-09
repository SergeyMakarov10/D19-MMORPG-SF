from django.urls import path
from .views import *


urlpatterns = [
   path('', HomePage.as_view(), name='mainpost'),
   path('post/', PostList.as_view(), name='post'),
   path('my_post/', MyPostList.as_view(), name='my_post'),
   path('my_post/<int:pk>/', MyPostDetail.as_view(), name='my_post_detail'),

   path('post/create/', PostCreate.as_view(), name='post_create'),
   path('post/<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('post/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('post/comment/create/', CommentCreate.as_view(), name='comment_create'),
   path('post/person_cabinet/', PersonCabinet.as_view(), name='person_cabinet'),
   path('post/comment/<int:pk>/comment_accept/', comment_accept, name='comment_accept'),
   path('post/comment/<int:pk>/comment_delete/', comment_delete, name='comment_delete'),

   path('categories/', CategoryName.as_view(),name='category_name'),
   path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
   path('categories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
]