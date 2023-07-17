const chatRoomName = document.querySelector('.chat-room-name');
const messageList = document.querySelector('.message-list');
const messageInput = document.querySelector('.message-send-input');
const sendButton = document.querySelector('.message-send-button');

const socketProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const socketURL = socketProtocol + window.location.host + '/ws/chat_room/' + chatRoomName.getAttribute("data-pk") + '/';

// Create a new WebSocket connection
const socket = new WebSocket(socketURL);
// Get sender and receiver
const senderId = sendButton.getAttribute('data-sender-pk');
const senderUsername = sendButton.getAttribute('data-sender-username');
const senderImgUrl = sendButton.getAttribute('data-sender-img');

const receiverId = sendButton.getAttribute('data-receiver-pk');
const receiverUsername = sendButton.getAttribute('data-receiver-username');
const receiverImgUrl = sendButton.getAttribute('data-receiver-img')


// WebSocket event listeners
socket.onopen = () => {
    messageList.scrollTop = messageList.scrollHeight;
    console.log('WebSocket connection established.');
};

socket.onmessage = (event) => {
    // Handle incoming WebSocket messages
    const message = JSON.parse(event.data);
    console.log('Received message:', message);
    const container = document.createElement('div');
    const img = document.createElement('img');
    const messageItem = document.createElement('li');

    if (message.sender === senderUsername) {
        container.className = 'sender-container';
        img.className = 'sender-img img-thumbnail img-fluid shadow';
        img.src = senderImgUrl;
        messageItem.className = 'message-item sender-message';
    } else {
        container.className = 'receiver-container';
        img.className = 'receiver-img img-thumbnail img-fluid shadow';
        img.src = receiverImgUrl;
        messageItem.className = 'message-item receiver-message';
    }
    container.appendChild(img);
    messageItem.textContent = message.message;
    container.appendChild(messageItem);
    messageList.appendChild(container);
    messageList.scrollTop = messageList.scrollHeight; // Scroll to the bottom of the message list
};

socket.onclose = () => {
    console.log('WebSocket connection closed.');
};

socket.onerror = (error) => {
    console.error('WebSocket error:', error);
};

sendButton.addEventListener('click', () => {
    const messageText = messageInput.value;
    if (messageText.trim() !== '') {
        sendMessage(messageText);
    }
});

function sendMessage(messageText) {
    const message = {
        sender_id: senderId,  // Replace 'Username' with the actual sender's username
        message: messageText,
    };
    socket.send(JSON.stringify(message));
    messageInput.value = ''; // Clear the input field
}

// Display Following list
const friendsLink = document.querySelector('.friends-link');
const leftColumn = document.querySelector('.left-column');

friendsLink.addEventListener('click', () => {
    leftColumn.classList.toggle('fade-in');
    leftColumn.classList.toggle('fade-out');
})

const friendItems = document.querySelectorAll('.friend-item');
friendItems.forEach(function (frienditem) {
    frienditem.addEventListener('click', function (event) {
        event.preventDefault();
        window.location.href = frienditem.querySelector('.friend-title').getAttribute('href');
    });
});

const chatRoomItems = document.querySelectorAll('.chat-room-item');
chatRoomItems.forEach(function (chatRoomitem) {
    chatRoomitem.addEventListener('click', function (event) {
        event.preventDefault();
        window.location.href = chatRoomitem.querySelector('.chat-room-title').getAttribute('href');
    });
});
