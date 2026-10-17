const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

exports.handler = async (event) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  let data;
  try {
    data = JSON.parse(event.body);
  } catch (err) {
    return { statusCode: 400, body: 'Invalid JSON' };
  }

  const { priceId } = data;
  if (!priceId) {
    return { statusCode: 400, body: 'Missing priceId' };
  }

  try {
    const session = await stripe.checkout.sessions.create({
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: `${process.env.URL || 'https://YOUR-SITE.netlify.app'}/success.html`,
      cancel_url: `${process.env.URL || 'https://YOUR-SITE.netlify.app'}/product.html`,
      shipping_options: [
        {
          shipping_rate: 'shr_1URSy5JAOBREUPrpPq8iUGAU',
        },
      ],
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ id: session.id, client_secret: session.client_secret }),
    };
  } catch (err) {
    console.error('Stripe error:', err);
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};