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
    const englishPath = `https://tokiidea.com/${pageName}`;
    const slovenianPath = `https://tokiidea.si/${pageName}`;
    const query = new URLSearchParams(window.location.search);
    query.delete('tokiidea_language');
    const cart = localStorage.getItem('tkiidea-cart');
    if (cart) {
        try {
            const items = JSON.parse(cart)
                .filter((item) => item?.productKey === 'kori' && Number.isInteger(item.quantity) && item.quantity > 0)
                .map(({ productKey, quantity }) => ({ productKey, quantity }));
            if (items.length) query.set('tokiidea_cart', btoa(JSON.stringify(items)));
        } catch (error) {
            console.error('Could not preserve cart while changing language:', error);
        }
    }
    const appendQuery = (url, language) => {
        const nextQuery = new URLSearchParams(query);
        nextQuery.set('tokiidea_language', language);
        return `${url}?${nextQuery.toString()}`;
    };

    document.querySelectorAll('.language-toggle').forEach((toggle) => {
        const englishLabel = document.createElement(isSlovenian ? 'a' : 'span');
        englishLabel.className = isSlovenian ? 'language-toggle-link' : 'language-toggle-current';
        englishLabel.lang = 'en';
        englishLabel.textContent = 'EN';
        englishLabel.setAttribute('aria-current', isSlovenian ? 'false' : 'true');

        if (isSlovenian) {
            englishLabel.href = appendQuery(englishPath, 'en');
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
            slovenianLabel.href = appendQuery(slovenianPath, 'sl');
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

    const cartTransfer = new URLSearchParams(window.location.search).get('tokiidea_cart');
    if (cartTransfer) {
        try {
            const transferredItems = JSON.parse(atob(cartTransfer));
            if (Array.isArray(transferredItems)) {
                const validItems = transferredItems.filter((item) =>
                    item?.productKey === 'kori' &&
                    Number.isInteger(item.quantity) &&
                    item.quantity > 0 &&
                    item.quantity <= 99
                );
                if (validItems.length) {
                    localStorage.setItem('tkiidea-cart', JSON.stringify(validItems.map((item) => ({
                        ...item,
                        name: 'Kori',
                        price: 3300
                    }))));
                    window.dispatchEvent(new Event('storage'));
                }
            }
        } catch (error) {
            console.error('Could not restore cart after changing language:', error);
        }

        const cleanUrl = new URL(window.location.href);
        cleanUrl.searchParams.delete('tokiidea_cart');
        cleanUrl.searchParams.delete('tokiidea_language');
        window.history.replaceState({}, '', cleanUrl);
    }
})();
