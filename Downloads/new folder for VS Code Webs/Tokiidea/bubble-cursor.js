const supportsBubbleCursor = window.matchMedia('(pointer: fine) and (hover: hover)');

if (supportsBubbleCursor.matches) {
  const bubble = document.createElement('div');
  bubble.className = 'bubble-cursor';
  bubble.setAttribute('aria-hidden', 'true');
  document.documentElement.appendChild(bubble);
  document.body.classList.add('has-bubble-cursor');

  document.addEventListener('pointermove', (event) => {
    if (event.pointerType !== 'mouse' && event.pointerType !== 'pen') {
      return;
    }

    bubble.style.transform = `translate3d(${event.clientX - 11}px, ${event.clientY - 11}px, 0)`;
    bubble.classList.add('bubble-cursor-visible');
  });

  document.addEventListener('pointerover', (event) => {
    if (event.target instanceof Element && event.target.closest('a, button, [role="button"]')) {
      bubble.classList.add('bubble-cursor-interactive');
    }
  });

  document.addEventListener('pointerout', (event) => {
    if (
      event.target instanceof Element &&
      event.target.closest('a, button, [role="button"]') &&
      (!(event.relatedTarget instanceof Element) || !event.relatedTarget.closest('a, button, [role="button"]'))
    ) {
      bubble.classList.remove('bubble-cursor-interactive');
    }
  });

  document.addEventListener('pointerleave', () => {
    bubble.classList.remove('bubble-cursor-visible', 'bubble-cursor-interactive');
  });
}
