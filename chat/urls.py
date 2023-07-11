# urls.py
from django.urls import path
from .views import (
    ChatRoomListView,
    ChatRoomDetailView,
    ChatRoomCreateView,
    ChatRoomUpdateView,
    ChatRoomDeleteView,
    # ChatMessageView,
)

urlpatterns = [
    path('chat_rooms/', ChatRoomListView.as_view(), name='chat-room-list'),
    path('chat_room/<int:pk>/', ChatRoomDetailView.as_view(),
         name='chat-room-detail'),
    path('chat_room/create/', ChatRoomCreateView.as_view(), name='chat-room-create'),
    path('chat_room/<int:pk>/update/',
         ChatRoomUpdateView.as_view(), name='chat-room-update'),
    path('chat_room/<int:pk>/delete/',
         ChatRoomDeleteView.as_view(), name='chat-room-delete'),
    #     path('chat_room/<int:pk>/messages/',
    #          ChatMessageView.as_view(), name='chat-room-messages'),
]
