from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    CommentView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    #     UserPostListView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    #     path('user/<str:username>/posts',
    #          UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/comment/create',
         CommentView.as_view(), name='comment-create'),
    path('post/<int:pk>/comment/<int:comment_pk>/reply',
         CommentView.as_view(), name='comment-reply'),
    path('post/<int:pk>/comment/<int:comment_pk>/update',
         CommentView.as_view(), name='comment-update'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('search/', views.search, name='search'),
]
