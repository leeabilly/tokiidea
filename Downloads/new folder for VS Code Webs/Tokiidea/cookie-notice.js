(() => {
  const dismissedKey = 'tokiidea-cookie-notice-dismissed';
  const isSlovenian = document.documentElement.lang === 'sl';
  let isDismissed = false;

  try {
    isDismissed = sessionStorage.getItem(dismissedKey) === 'true';
  } catch (error) {
    console.warn('Could not read cookie notice preference:', error);
  }

  const notice = document.createElement('aside');
  notice.className = 'cookie-notice';
  notice.setAttribute('aria-label', isSlovenian ? 'Podatki o piškotkih in shrambi' : 'Cookie and storage information');
  notice.setAttribute('role', 'status');

  const message = document.createElement('p');
  message.textContent = isSlovenian
    ? 'Ta trgovina uporablja nujno shrambo brskalnika za košarico in prikaz izdelkov. Analitičnih ali oglaševalskih piškotkov ne uporabljamo.'
    : 'This shop uses essential browser storage for your cart and product display. We do not use analytics or advertising cookies.';

  const policyLink = document.createElement('a');
  policyLink.href = isSlovenian ? 'cookies.html' : 'sl/cookies.html';
  policyLink.textContent = isSlovenian ? 'Pravilnik o piškotkih' : 'Cookie policy';

  const dismissButton = document.createElement('button');
  dismissButton.className = 'cookie-notice-dismiss';
  dismissButton.type = 'button';
  dismissButton.textContent = isSlovenian ? 'Razumem' : 'Got it';

  notice.append(message, policyLink, dismissButton);
  document.body.append(notice);

  const dismiss = () => {
    notice.hidden = true;
    try {
      sessionStorage.setItem(dismissedKey, 'true');
    } catch (error) {
      console.warn('Could not save cookie notice preference:', error);
    }
  };

  dismissButton.addEventListener('click', dismiss);
  notice.hidden = isDismissed;

  document.getElementById('show-cookie-notice')?.addEventListener('click', () => {
    notice.hidden = false;
  });
})();
