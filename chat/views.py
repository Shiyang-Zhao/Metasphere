# views.py
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from users.models import Profile
from .models import ChatRoom, ChatMessage
from django.contrib.auth.models import User
from django.db.models import Q


class ChatRoomListView(LoginRequiredMixin, ListView):
    model = ChatRoom
    template_name = 'chat_rooms.html'
    context_object_name = 'chat_rooms'

    def get_queryset(self):
        # Return a queryset containing chat rooms that the logged-in user is a member of.
        return ChatRoom.objects.filter(members__in=[self.request.user])


class ChatRoomDetailView(LoginRequiredMixin, DetailView):
    model = ChatRoom
    template_name = 'chat_room_detail.html'
    context_object_name = 'chat_room'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chat_rooms'] = ChatRoom.objects.filter(
            members=self.request.user)
        # Add the logged-in user to the context
        context['sender'] = get_object_or_404(Profile, user=self.request.user)
        chat_room = self.get_object()
        receiver = chat_room.members.exclude(
            username=self.request.user.username).first()
        context['receiver'] = get_object_or_404(Profile, user=receiver)
        return context


class ChatRoomCreateView(LoginRequiredMixin, CreateView):
    model = ChatRoom
    fields = []

    def form_valid(self, form):

        sender = self.request.user
        receiver = get_object_or_404(
            User, pk=self.request.POST.get('receiver_id'))
        existing_chat_room = ChatRoom.objects.filter(
            members=sender).filter(members=receiver).filter(
                is_direct_message=True).first()

        if existing_chat_room:
            chat_room = existing_chat_room
        else:
            chat_room = form.save(commit=False)
            chat_room.name = receiver.username
            chat_room.is_direct_message = True
            chat_room.save()
            chat_room.members.add(sender, receiver)

        return redirect('chat-room-detail', pk=chat_room.pk)


class ChatRoomUpdateView(LoginRequiredMixin, UpdateView):
    model = ChatRoom
    fields = ['name', 'is_direct_message']


class ChatRoomDeleteView(LoginRequiredMixin, DeleteView):
    model = ChatRoom
    success_url = '/chat/chat_rooms/'  # Redirect to the home page after deletion


# class ChatMessageView(LoginRequiredMixin, DetailView):
#     model = ChatRoom
#     template_name = 'chat_room_detail.html'
#     context_object_name = 'chat_room'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         chat_room = self.get_object()
#         # Retrieve all messages for the chat room and pass them to the template
#         context['messages'] = chat_room.messages.all()
#         return context
