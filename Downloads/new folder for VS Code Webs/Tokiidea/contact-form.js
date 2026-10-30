(() => {
  const form = document.getElementById('contact-form');
  const status = document.getElementById('form-status');
  const submitButton = form?.querySelector('button[type="submit"]');

  if (!form || !status || !submitButton) return;

  const isSlovenian = document.documentElement.lang === 'sl';

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    status.textContent = '';
    submitButton.disabled = true;

    try {
      const response = await fetch('https://toki-idea.netlify.app/.netlify/functions/send-contact-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: form.elements.name.value,
          email: form.elements.email.value,
          message: form.elements.message.value,
          botField: form.elements['bot-field'].value,
        }),
      });
      const result = await response.json();

      if (!response.ok || !result.ok) {
        throw new Error(result.error || 'The message could not be sent.');
      }

      form.reset();
      status.textContent = isSlovenian
        ? 'Hvala! Vaše sporočilo je bilo poslano.'
        : 'Thank you! Your message has been sent.';
    } catch (error) {
      console.error('Contact form error:', error);
      status.textContent = isSlovenian
        ? 'Sporočila ni bilo mogoče poslati. Poskusite znova pozneje.'
        : 'Your message could not be sent. Please try again later.';
    } finally {
      submitButton.disabled = false;
    }
  });
})();
