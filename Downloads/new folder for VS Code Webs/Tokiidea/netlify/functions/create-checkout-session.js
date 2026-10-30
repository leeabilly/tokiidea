const allowedOrigins = new Set(
  (process.env.CHECKOUT_ALLOWED_ORIGINS ||
    'https://tokiidea.com,https://www.tokiidea.com,https://leeabilly.github.io')
    .split(',')
    .map((origin) => origin.trim())
    .filter(Boolean)
);

const jsonResponse = (statusCode, body, origin) => ({
  statusCode,
  headers: {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-store',
    'Vary': 'Origin',
    ...(origin && allowedOrigins.has(origin)
      ? {
          'Access-Control-Allow-Origin': origin,
          'Access-Control-Allow-Methods': 'POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        }
      : {}),
  },
  body: body === null ? '' : JSON.stringify(body),
});

exports.handler = async (event) => {
  const origin = event.headers?.origin || event.headers?.Origin;

  if (event.httpMethod === 'OPTIONS') {
    return origin && allowedOrigins.has(origin)
      ? jsonResponse(204, null, origin)
      : jsonResponse(403, { error: 'Origin is not allowed.' });
  }

  if (event.httpMethod !== 'POST') {
    return jsonResponse(405, { error: 'Method not allowed.' }, origin);
  }

  if (!origin || !allowedOrigins.has(origin)) {
    return jsonResponse(403, { error: 'Origin is not allowed.' });
  }

  const secretKey = process.env.STRIPE_SECRET_KEY;
  const allowedPriceIds = new Set(
    (process.env.STRIPE_ALLOWED_PRICE_IDS || '')
      .split(',')
      .map((priceId) => priceId.trim())
      .filter(Boolean)
  );
  const shippingRateId = process.env.STRIPE_SHIPPING_RATE_ID;

  if (!secretKey || !/^sk_(test|live)_/.test(secretKey)) {
    console.error('Stripe checkout is unavailable: a valid Stripe secret key is not configured.');
    return jsonResponse(500, { error: 'Checkout is not configured. Please try again later.' }, origin);
  }

  if (allowedPriceIds.size === 0 || !shippingRateId) {
    console.error('Stripe checkout is unavailable: allowed prices or shipping rate are not configured.');
    return jsonResponse(500, { error: 'Checkout is not configured. Please try again later.' }, origin);
  }

  let data;
  try {
    data = JSON.parse(event.body || '');
  } catch {
    return jsonResponse(400, { error: 'Invalid JSON.' }, origin);
  }

  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    return jsonResponse(400, { error: 'Invalid cart items.' }, origin);
  }

  const requestedItems = Array.isArray(data.line_items)
    ? data.line_items
    : data.priceId
      ? [{ price: data.priceId, quantity: 1 }]
      : [];

  if (
    requestedItems.length === 0 ||
    requestedItems.some((item) =>
      !item ||
      typeof item !== 'object' ||
      !allowedPriceIds.has(item.price) ||
      !Number.isInteger(item.quantity) ||
      item.quantity < 1 ||
      item.quantity > 99
    )
  ) {
    return jsonResponse(400, { error: 'Cart items are invalid.' }, origin);
  }

  try {
    const form = new URLSearchParams({
      mode: 'payment',
      'success_url': 'https://tokiidea.com/success.html?session_id={CHECKOUT_SESSION_ID}',
      'cancel_url': 'https://tokiidea.com/cart.html',
      'shipping_address_collection[allowed_countries][0]': 'SI',
      'shipping_options[0][shipping_rate]': shippingRateId,
    });

    requestedItems.forEach(({ price, quantity }, index) => {
      form.set(`line_items[${index}][price]`, price);
      form.set(`line_items[${index}][quantity]`, String(quantity));
    });

    const stripeResponse = await fetch('https://api.stripe.com/v1/checkout/sessions', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${secretKey}`,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: form,
    });
    const session = await stripeResponse.json();

    if (!stripeResponse.ok || !session.url) {
      console.error('Stripe checkout session creation failed:', stripeResponse.status, session.error?.code);
      return jsonResponse(502, {
        error: 'Stripe could not start checkout. Check the Stripe key, allowed price IDs, and shipping rate configuration.',
      }, origin);
    }

    return jsonResponse(200, { id: session.id, url: session.url }, origin);
  } catch (err) {
    console.error('Stripe checkout request failed:', err);
    return jsonResponse(500, {
      error: 'Stripe could not start checkout. Check the Stripe key, allowed price IDs, and shipping rate configuration.',
    }, origin);
  }
};