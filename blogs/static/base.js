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


