const checkboxes = document.querySelectorAll('.friend-checkbox');
const createGroupChatButton = document.querySelector('.create-group-chat');
const createButton = document.querySelector('.create');
const leftColumn = document.querySelector('.left-column');

// Display Following list
createGroupChatButton.addEventListener('click', () => {
    leftColumn.classList.toggle('fade-in');
    leftColumn.classList.toggle('fade-out');
})

// Add event listener to each checkbox
checkboxes.forEach((checkbox) => {
    checkbox.addEventListener('change', () => {
        const checkedCount = document.querySelectorAll('.friend-checkbox:checked').length;
        console.log(checkedCount);
        if (checkedCount > 0) {
            createGroupChatButton.classList.remove('zoom-in');
            createGroupChatButton.classList.add('zoom-out');
            createButton.classList.remove('zoom-out');
            createButton.classList.add('zoom-in');
            createButton.style.visibility = 'visible';
        } else {
            createButton.classList.remove('zoom-in');
            createButton.classList.add('zoom-out');
            createGroupChatButton.classList.remove('zoom-out');
            createGroupChatButton.classList.add('zoom-in');
            createButton.style.visibility = 'hidden';
        }
    });
});

function getCheckedFirends() {
    const checkedBoxes = document.querySelectorAll('.friend-checkbox:checked');
    const receiverIds = Array.from(checkedBoxes).map(function (checkbox) {
        return checkbox.value;
    }).join(',');
    document.querySelector('.receiver-ids-input').value = receiverIds;
    checkedBoxes.forEach(function (checkbox) {
        checkbox.checked = false;
    });
}

function toggleCheckbox(checkboxId) {
    var checkbox = document.getElementById(checkboxId);
    checkbox.checked = !checkbox.checked;
}

const chatRoomItems = document.querySelectorAll('.chat-room-item');
chatRoomItems.forEach(function (chatRoomitem) {
    chatRoomitem.addEventListener('click', function (event) {
        event.preventDefault();
        window.location.href = chatRoomitem.querySelector('.chat-room-title').getAttribute('href');
    });
});
