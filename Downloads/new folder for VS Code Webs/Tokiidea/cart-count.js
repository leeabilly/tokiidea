document.addEventListener('DOMContentLoaded', updateCartCount);
window.addEventListener('storage', (event) => {
  if (event.key === 'tkiidea-cart') {
    updateCartCount();
  }
});

let cartFeedbackTimeout;

window.animateCartFeedback = (trigger) => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const cartBasket = document.querySelector('.cart-basket');
  const cartCount = document.querySelector('.cart-count');
  const cartIcon = cartBasket?.querySelector('svg');
  if (!trigger || !cartBasket || !cartCount || !cartIcon) return;

  window.clearTimeout(cartFeedbackTimeout);

  const triggerBounds = trigger.getBoundingClientRect();
  const basketBounds = cartIcon.getBoundingClientRect();
  const startX = triggerBounds.left + triggerBounds.width / 2;
  const startY = triggerBounds.top + triggerBounds.height / 2;
  const deltaX = basketBounds.left + basketBounds.width / 2 - startX;
  const deltaY = basketBounds.top + basketBounds.height / 2 - startY;
  const bubble = document.createElement('span');

  bubble.className = 'cart-flight-bubble';
  bubble.setAttribute('aria-hidden', 'true');
  bubble.style.left = `${startX - 6}px`;
  bubble.style.top = `${startY - 6}px`;
  document.body.append(bubble);

  const animation = bubble.animate([
    { opacity: 0, transform: 'translate(0, 0) scale(0.55)' },
    {
      opacity: 0.8,
      transform: `translate(${deltaX * 0.48}px, ${deltaY * 0.48 - 18}px) scale(0.9)`,
      offset: 0.55
    },
    { opacity: 0.95, transform: `translate(${deltaX}px, ${deltaY}px) scale(0.35)` }
  ], {
    duration: 1050,
    easing: 'cubic-bezier(0.22, 0.68, 0.28, 1)',
    fill: 'forwards'
  });

  animation.onfinish = () => {
    bubble.remove();
    cartBasket.classList.remove('cart-added');
    cartCount.classList.remove('cart-count-added');
    void cartIcon.offsetWidth;
    cartBasket.classList.add('cart-added');
    cartCount.classList.add('cart-count-added');

    cartFeedbackTimeout = window.setTimeout(() => {
      cartBasket.classList.remove('cart-added');
      cartCount.classList.remove('cart-count-added');
    }, 500);
  };

  animation.oncancel = () => bubble.remove();
};

function updateCartCount() {
  const cartCount = document.querySelector('.cart-count');
  const cartBasket = document.querySelector('.cart-basket');
  if (!cartCount || !cartBasket) return;
  const isSlovenian = document.documentElement.lang === 'sl';

  let cart;
  try {
    cart = JSON.parse(localStorage.getItem('tkiidea-cart') || '[]');
  } catch (error) {
    console.error('Could not read cart contents:', error);
    return;
  }

  if (!Array.isArray(cart)) {
    console.error('Could not read cart contents: expected an array.');
    return;
  }

  const count = cart.reduce((total, item) => {
    const quantity = Number(item?.quantity);
    return total + (Number.isFinite(quantity) && quantity > 0 ? quantity : 0);
  }, 0);

  cartCount.textContent = count;
  cartCount.style.display = count > 0 ? 'flex' : 'none';
  if (isSlovenian) {
    const itemLabel = count === 1 ? 'izdelek' : count >= 2 && count <= 4 ? 'izdelki' : 'izdelkov';
    cartBasket.setAttribute('aria-label', `Košarica, ${count} ${itemLabel}`);
  } else {
    cartBasket.setAttribute('aria-label', `Cart, ${count} ${count === 1 ? 'item' : 'items'}`);
  }
}
