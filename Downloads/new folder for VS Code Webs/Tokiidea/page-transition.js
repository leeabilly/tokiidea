const productPageUrl = new URL('product.html', window.location.href);

document.querySelectorAll('a[href="product.html"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey ||
      link.target ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches
    ) {
      return;
    }

    event.preventDefault();
    sessionStorage.setItem('tokiidea-product-transition', 'true');
    document.body.classList.add('product-transition-leave');
    window.setTimeout(() => window.location.assign(productPageUrl), 180);
  });
});

if (
  window.location.pathname === productPageUrl.pathname &&
  sessionStorage.getItem('tokiidea-product-transition') === 'true'
) {
  sessionStorage.removeItem('tokiidea-product-transition');
  document.body.classList.add('product-transition-enter');
  requestAnimationFrame(() => {
    document.body.classList.add('product-transition-ready');
  });
}

window.addEventListener('pageshow', () => {
  document.body.classList.remove('product-transition-leave');
});
