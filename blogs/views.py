from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment
import operator
from django.urls import reverse, reverse_lazy
from django.contrib.staticfiles.views import serve

from django.db.models import Q


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'home.html', context)


def search(request):
    template = 'home.html'

    query = request.GET.get('q')

    result = Post.objects.filter(Q(title__icontains=query) | Q(
        author__username__icontains=query) | Q(content__icontains=query))
    paginate_by = 5

    context = {'posts': result}
    return render(request, template, context)


def getfile(request):
    return serve(request, 'File')


class PostListView(ListView):
    model = Post
    template_name = 'home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(
            post=self.get_object(), parent_comment=None).order_by('date_posted')
        context['comments'] = comments
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = Comment.objects.filter(
            post=post, parent_comment=None).order_by('date_posted')
        context['comments'] = comments
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            resolver_match = request.resolver_match
            if resolver_match.url_name == 'comment-create' or resolver_match.url_name == 'comment-reply':
                post = self.get_object()
                content = request.POST.get('content')
                parent_comment_pk = request.POST.get('parent_comment_pk')
                parent_comment = None
                if parent_comment_pk:
                    parent_comment = Comment.objects.get(pk=parent_comment_pk)

                if not content:
                    return redirect('post-detail', post.pk)
                comment = Comment.objects.create(
                    post=post, author=request.user, content=content, parent_comment=parent_comment)
                comment.save()

            elif resolver_match.url_name == 'comment-update':
                comment_pk = request.POST.get('comment_pk')
                content = request.POST.get('content')

                if comment_pk and content:
                    comment = get_object_or_404(Comment, pk=comment_pk)
                    comment.content = content
                    comment.save()

        return redirect(self.request.path_info)
