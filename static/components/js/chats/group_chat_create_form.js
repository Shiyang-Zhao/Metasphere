document.addEventListener('DOMContentLoaded', function () {
    const modalButton = document.querySelector('#openModalButton');
    const myModalElement = document.querySelector('#myModal');
    const myModal = new bootstrap.Modal(myModalElement, {
        keyboard: false
    });
    const createChatButton = document.querySelector('#create-chat-button')
    const createChatButtonPopover = new bootstrap.Popover(createChatButton, {
        trigger: 'manual',
        html: true,
        content: 'You must select at least one participant',
        placement: 'right',
    });

    modalButton.addEventListener('click', function () {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.set('group_chat_create_form', 'open');
        window.history.pushState({}, '', window.location.pathname + '?' + urlParams.toString());
        myModal.show();
    });

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('group_chat_create_form') === 'open') {
        myModal.show();
    }

    myModalElement.addEventListener('hidden.bs.modal', function () {
        const urlParams = new URLSearchParams(window.location.search);
        urlParams.delete('group_chat_create_form');
        let newUrl = window.location.pathname;
        if (urlParams.toString()) {
            newUrl += '?' + urlParams.toString();
        }
        window.history.pushState({}, '', newUrl);
    });

    document.querySelector('#group-chat-create-form').addEventListener('submit', function (event) {
        const checkboxes = document.querySelectorAll('.participant-checkbox');
        const isChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);

        if (!isChecked) {
            event.preventDefault();
            createChatButtonPopover.show();
            setTimeout(() => { createChatButtonPopover.hide(); }, 3000);
        }
    });

    document.querySelectorAll('.participant-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (document.querySelector('.participant-checkbox:checked')) {
                createChatButtonPopover.hide();
            }
        });
    });
});

