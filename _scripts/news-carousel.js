// Initialize news carousel with Swiper.js
// Runs after DOM is loaded and Swiper library is available

window.addEventListener('DOMContentLoaded', () => {
  // Check if Swiper is available and carousel element exists
  if (typeof Swiper === 'undefined') {
    console.warn('Swiper library not loaded');
    return;
  }

  const carouselElement = document.querySelector('.news-carousel');
  if (!carouselElement) {
    // Carousel not present on this page, exit silently
    return;
  }

  // Check reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Initialize Swiper
  const newsCarousel = new Swiper('.news-carousel', {
    // Loop mode for continuous navigation
    loop: true,

    // Keyboard navigation
    keyboard: {
      enabled: true,
      onlyInViewport: true,
    },

    // Navigation arrows
    navigation: {
      nextEl: '.news-carousel-next',
      prevEl: '.news-carousel-prev',
    },

    // Pagination dots
    pagination: {
      el: '.news-carousel-pagination',
      clickable: true,
      type: 'bullets',
    },

    // Accessibility
    a11y: {
      enabled: true,
      prevSlideMessage: 'Previous news item',
      nextSlideMessage: 'Next news item',
      paginationBulletMessage: 'Go to news item {{index}}',
    },

    // Autoplay configuration
    autoplay: prefersReducedMotion ? false : {
      delay: 5000,
      disableOnInteraction: false,
      pauseOnMouseEnter: true,
    },

    // Respect reduced motion preference
    effect: 'slide',
    speed: prefersReducedMotion ? 0 : 300,
  });

  // Manually start autoplay for Safari compatibility
  if (!prefersReducedMotion && newsCarousel.autoplay) {
    newsCarousel.autoplay.start();
  }
});
