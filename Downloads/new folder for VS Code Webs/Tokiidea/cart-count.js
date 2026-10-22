document.addEventListener('DOMContentLoaded', updateCartCount);
window.addEventListener('storage', (event) => {
  if (event.key === 'tkiidea-cart') {
    updateCartCount();
  }
});

function updateCartCount() {
  const cartCount = document.querySelector('.cart-count');
  const cartBasket = document.querySelector('.cart-basket');
  if (!cartCount || !cartBasket) return;

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
  cartBasket.setAttribute('aria-label', `Cart, ${count} ${count === 1 ? 'item' : 'items'}`);
}
