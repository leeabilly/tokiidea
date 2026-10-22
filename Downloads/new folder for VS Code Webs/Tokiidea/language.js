(() => {
    const pageNames = new Set([
        'index.html',
        'product.html',
        'cart.html',
        'contact.html',
        'faq.html',
        'shipping.html',
        'returns.html',
        'privacy.html',
        'terms.html',
        'cookies.html',
        'success.html'
    ]);
    const isSlovenian = document.documentElement.lang === 'sl';
    const pathParts = window.location.pathname.split('/');
    const fileName = pathParts.pop() || 'index.html';
    const pageName = pageNames.has(fileName) ? fileName : 'index.html';
    const englishPath = `/${pageName}`;
    const slovenianPath = `/sl/${pageName}`;

    document.querySelectorAll('.language-toggle').forEach((toggle) => {
        const englishLabel = document.createElement(isSlovenian ? 'a' : 'span');
        englishLabel.className = isSlovenian ? 'language-toggle-link' : 'language-toggle-current';
        englishLabel.lang = 'en';
        englishLabel.textContent = 'EN';
        englishLabel.setAttribute('aria-current', isSlovenian ? 'false' : 'true');

        if (isSlovenian) {
            englishLabel.href = englishPath;
            englishLabel.dataset.languageChoice = 'en';
        }

        const divider = document.createElement('span');
        divider.className = 'language-toggle-divider';
        divider.setAttribute('aria-hidden', 'true');
        divider.textContent = '·';

        const slovenianLabel = document.createElement(isSlovenian ? 'span' : 'a');
        slovenianLabel.className = isSlovenian ? 'language-toggle-current' : 'language-toggle-link';
        slovenianLabel.lang = 'sl';
        slovenianLabel.textContent = 'SL';
        slovenianLabel.setAttribute('aria-current', isSlovenian ? 'true' : 'false');

        if (!isSlovenian) {
            slovenianLabel.href = slovenianPath;
            slovenianLabel.dataset.languageChoice = 'sl';
        }

        toggle.setAttribute('aria-label', isSlovenian ? 'Jezik' : 'Language');
        toggle.replaceChildren(englishLabel, divider, slovenianLabel);
    });

    document.querySelectorAll('[data-language-choice]').forEach((link) => {
        link.addEventListener('click', () => {
            const secure = window.location.protocol === 'https:' ? '; Secure' : '';
            document.cookie = `tokiidea-language=${link.dataset.languageChoice}; Path=/; Max-Age=31536000; SameSite=Lax${secure}`;
        });
    });
})();
