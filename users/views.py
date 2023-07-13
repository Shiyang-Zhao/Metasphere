from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from blogs.models import Post

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile', username=username)
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    context = {
        'user': user,
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profile.html', context)


@login_required
def manage_friend(request, username):
    friend = get_object_or_404(User, username=username)
    profile = request.user.profile

    if profile.following.filter(user=friend).exists():
        # Friend already exists, remove them
        profile.following.remove(friend.profile)
        messages.success(
            request, f"You have removed {friend.username} as a friend.")
    else:
        # Friend doesn't exist, add them
        profile.following.add(friend.profile)
        messages.success(
            request, f"You have added {friend.username} as a friend.")

    return redirect('profile', username=friend.username)
