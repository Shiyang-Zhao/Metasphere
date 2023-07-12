// base.js

// Function to add a fade-in and scale effect when the page loads
function fadeInAndScalePage() {
   // Select the main container
   const container = document.querySelector('.background-container');

   // Check if the container exists (optional, but recommended)
   if (container) {
      // Add a CSS class to apply the fade-in and scale effect
      container.classList.add('fade-in-scale');
   }
}

// Call the fadeInAndScalePage function when the page finishes loading
window.onload = fadeInAndScalePage;

//Comment and Reply//
const commentHeader = document.querySelectorAll('.comment-header');
const replyLinks = document.querySelectorAll('.reply-link');
const updateLinks = document.querySelectorAll('.update-link');
const imgLinks = document.querySelectorAll('.img-link');
const authorLinks = document.querySelectorAll('.author-link');

commentHeader.forEach(function (header) {
   header.addEventListener('click', function (event) {
      event.preventDefault();
      const replyForm = header.nextElementSibling;
      replyForm.style.display = replyForm.style.display === 'block' ? 'none' : 'block';
   });
});

replyLinks.forEach(function (replyLink) {
   replyLink.addEventListener('click', function (event) {
      event.preventDefault();
      event.stopPropagation();
      const replyForm = replyLink.closest('.comments-replies').querySelector('.reply-form');
      replyForm.style.display = replyForm.style.display === 'block' ? 'none' : 'block';

   });
});

updateLinks.forEach(function (updateLink) {
   updateLink.addEventListener('click', function (event) {
      event.preventDefault();
      event.stopPropagation();
      const updateForm = updateLink.closest('.comments-replies').querySelector('.update-form');
      updateForm.style.display = updateForm.style.display === 'block' ? 'none' : 'block';
   });
});

imgLinks.forEach(function (imgLink) {
   imgLink.addEventListener('click', function (event) {
      event.stopPropagation();
   });
});

authorLinks.forEach(function (authorLink) {
   authorLink.addEventListener('click', function (event) {
      event.stopPropagation();
   });
});


