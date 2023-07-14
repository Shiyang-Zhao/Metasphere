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
        # Add the logged-in user to the context
        chat_room = self.get_object()
        context['sender'] = get_object_or_404(Profile, user=self.request.user)
        receiver = chat_room.members.exclude(
            username=self.request.user.username).first()
        context['receiver'] = get_object_or_404(Profile, user=receiver)
        return context


class ChatRoomCreateView(LoginRequiredMixin, CreateView):
    model = ChatRoom
    fields = []

    def form_valid(self, form):
        is_direct_message = self.request.POST.get(
            'is_direct_message') == 'True'
        sender = self.request.user
        if is_direct_message:
            # Handle direct message creation
            receiver = get_object_or_404(
                User, pk=self.request.POST.get('receiver_id'))
            members = [sender, receiver]
            existing_chat_room = sender.chat_rooms.filter(members=sender).filter(
                members=receiver, is_direct_message=True).first()

            if existing_chat_room:
                chat_room = existing_chat_room
            else:
                chat_room = form.save()
                chat_room.name = receiver.username
                chat_room.is_direct_message = is_direct_message
                chat_room.members.set(members)
                chat_room.save()
        else:
            # Handle group chat creation
            receiver_ids = [int(id) for id in self.request.POST.get(
                'receiver_ids').split(',')]
            receivers = User.objects.filter(pk__in=receiver_ids)
            members = [sender] + list(receivers)
            existing_chat_rooms = sender.chat_rooms.filter(
                members__in=members, is_direct_message=False)

            for existing_chat_room in existing_chat_rooms:
                if set(existing_chat_room.members.all()) == set(members):
                    return redirect('chat-room-detail', pk=existing_chat_room.pk)

            chat_room = form.save()
            chat_room.is_direct_message = is_direct_message
            chat_room.name = f"Group {chat_room.pk}"
            chat_room.members.set(members)
            chat_room.save()

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
