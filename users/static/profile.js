const userPosts = document.querySelectorAll('.user-post');
// const updateForm = document.querySelector('.profile-update-form');
// const editButton = document.querySelector('.edit-profile-btn');

// Add click event listener to each user-post element
userPosts.forEach((userPost) => {
  userPost.addEventListener('click', () => {
    window.location.href = userPost.dataset.url;
  });
});

const editProfileBtn = document.querySelector('.edit-profile-btn');
const profileUpdateForm = document.querySelector('.profile-update-form');
const overlay = document.querySelector('overlay');

editProfileBtn.addEventListener('click', function () {
  
});

function lazyLoad() {
  const lazyImages = document.querySelectorAll('.image-post.lazy');
  const lazyVideos = document.querySelectorAll('.video-post.lazy');

  const options = {
    root: null, // Use the viewport as the root element
    rootMargin: '0px', // No margin added
    threshold: 0.1 // Trigger at 10% of the element's visibility
  };

  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const image = entry.target;
        image.src = image.dataset.src;
        image.classList.remove('lazy');
        observer.unobserve(image);
      }
    });
  }, options);

  const videoObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const video = entry.target;
        video.src = video.dataset.src;
        video.classList.remove('lazy');
        observer.unobserve(video);
      }
    });
  }, options);

  lazyImages.forEach(image => {
    imageObserver.observe(image);
  });

  lazyVideos.forEach(video => {
    videoObserver.observe(video);
  });
}

// Call the lazyLoad function when the page finishes loading
window.addEventListener('load', lazyLoad);