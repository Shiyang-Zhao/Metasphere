const userPosts = document.querySelectorAll('.user-post');
// const updateForm = document.querySelector('.profile-update-form');
// const editButton = document.querySelector('.edit-profile-btn');

// Add click event listener to each user-post element
userPosts.forEach((userPost) => {
    userPost.addEventListener('click', () => {
        window.location.href = userPost.getAttribute('data-url');
    });
});

var editProfileBtn = document.querySelector('.edit-profile-btn');
  var profileUpdateForm = document.querySelector('.profile-update-form');

  editProfileBtn.addEventListener('click', function() {
    profileUpdateForm.classList.toggle('fade-out');
    profileUpdateForm.classList.toggle('fade-in');
    profileUpdateForm.style.left = '0'; // Move the form to the visible position
  });