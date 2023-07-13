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