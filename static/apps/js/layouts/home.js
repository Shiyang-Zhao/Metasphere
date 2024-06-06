import { handlePostSaveAndUnsaveButton } from "../../../components/js/posts/post_dropdown.js";
import { handlePostLikeAndDislikeButton } from "../../../components/js/posts/post_like_and_dislike_button.js";
import { handleStoryShowAndHideButton } from "../../../components/js/stories/story_item.js";

document.addEventListener('DOMContentLoaded', () => {
    const storiesContainer = document.querySelector('#stories-container');
    const sortSelect = document.querySelector('#sort-select');
    const postsContainer = document.querySelector('#posts-container');

    handleStoryShowAndHideButton(storiesContainer);
    handlePostSaveAndUnsaveButton(postsContainer);
    handlePostLikeAndDislikeButton(postsContainer);

    sortSelect.addEventListener('change', function () {
        window.location.href = this.value;
    });

    document.body.addEventListener('click', function (event) {
        if (event.target.matches('.dropdown-btn, .dropdown-btn *, .dropdown-item, .dropdown-menu, .card-author, .file-video, .file-download')) {
            event.stopPropagation();
            return;
        }
        const card = event.target.closest('.post-container');
        if (card) {
            window.location.href = card.getAttribute('data-href');
        }
    });
    document.addEventListener("DOMContentLoaded", () => {
    });
});

document.addEventListener('DOMContentLoaded', function () {
    let isFetchingPosts = false;
    let page = 1;
    let hasMorePosts = true;

    const postsContainer = document.querySelector('#posts-container');
    // Creating a sentinel element to observe
    const sentinel = document.createElement('div');
    postsContainer.appendChild(sentinel);

    function fetchPosts() {
        console.log('Fetching posts:', page);
        if (isFetchingPosts || !hasMorePosts) {
            console.log('Fetch prevented:', isFetchingPosts, hasMorePosts);
            return;
        }
        isFetchingPosts = true;

        const nextPage = page + 1;
        const url = new URL(window.location.href);
        url.searchParams.set('page', nextPage);

        axios.get(url.toString(), {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
            .then(response => {
                const html = response.data.html;
                hasMorePosts = response.data.has_more;
                console.log('Posts fetched:', nextPage, 'Has more posts:', hasMorePosts);
                if (html) {
                    sentinel.insertAdjacentHTML('beforebegin', html);
                    page = nextPage;
                } else {
                    console.log('No more posts to fetch, disconnecting observer.');
                    observer.disconnect();
                }
            })
            .catch(error => {
                console.error('Error fetching posts:', error);
            })
            .finally(() => {
                isFetchingPosts = false;
                console.log('Fetch complete, isFetching reset.');
            });
    }

    const observer = new IntersectionObserver(entries => {
        // Check if the sentinel is currently visible in the viewport
        if (entries[0].isIntersecting) {
            console.log('Sentinel visible, triggering fetch');
            fetchPosts();
        }
    }, {
        rootMargin: '0px',
        threshold: 0.1  // Adjust threshold to your needs
    });

    observer.observe(sentinel);
});