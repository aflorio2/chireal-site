// Dynamically set header height as CSS variable
function setHeaderHeight() {
  const header = document.querySelector('header');
  if (header) {
    const height = header.offsetHeight;
    document.documentElement.style.setProperty('--header-height', `${height}px`);
  }
}

// Set on load
window.addEventListener('load', setHeaderHeight);

// Update on resize
window.addEventListener('resize', setHeaderHeight);
