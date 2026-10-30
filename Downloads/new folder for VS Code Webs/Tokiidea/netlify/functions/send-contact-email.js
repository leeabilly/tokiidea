const allowedOrigins = new Set(
  (process.env.CONTACT_ALLOWED_ORIGINS ||
    'https://tokiidea.com,https://www.tokiidea.com,https://leeabilly.github.io')
    .split(',')
    .map((origin) => origin.trim())
    .filter(Boolean)
);

const response = (statusCode, body, origin) => ({
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

const escapeHtml = (value) => value.replace(/[&<>"']/g, (character) => ({
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
})[character]);

exports.handler = async (event) => {
  const origin = event.headers?.origin || event.headers?.Origin;

  if (event.httpMethod === 'OPTIONS') {
    return origin && allowedOrigins.has(origin)
      ? response(204, null, origin)
      : response(403, { error: 'Origin is not allowed.' });
  }

  if (event.httpMethod !== 'POST') {
    return response(405, { error: 'Method not allowed.' }, origin);
  }

  if (!origin || !allowedOrigins.has(origin)) {
    return response(403, { error: 'Origin is not allowed.' });
  }

  const apiKey = process.env.RESEND_API_KEY;
  const from = process.env.CONTACT_FROM_EMAIL;
  if (!apiKey || !from) {
    console.error('Contact email is unavailable: Resend credentials are not configured.');
    return response(500, { error: 'The contact form is temporarily unavailable. Please try again later.' }, origin);
  }

  let data;
  try {
    data = JSON.parse(event.body || '');
  } catch {
    return response(400, { error: 'Invalid form submission.' }, origin);
  }

  if (!data || typeof data !== 'object' || Array.isArray(data)) {
    return response(400, { error: 'Invalid form submission.' }, origin);
  }

  if (typeof data.botField === 'string' && data.botField.trim()) {
    return response(200, { ok: true }, origin);
  }

  const name = typeof data.name === 'string' ? data.name.trim() : '';
  const email = typeof data.email === 'string' ? data.email.trim() : '';
  const message = typeof data.message === 'string' ? data.message.trim() : '';

  if (
    name.length < 1 ||
    name.length > 120 ||
    email.length > 254 ||
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) ||
    message.length < 1 ||
    message.length > 5000
  ) {
    return response(400, { error: 'Enter a valid name, email address, and message.' }, origin);
  }

  try {
    const result = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from,
        to: ['lea.ideabylea@outlook.com'],
        reply_to: email,
        subject: `Tokiidea website message from ${name}`,
        text: `Name: ${name}\nEmail: ${email}\n\n${message}`,
        html: `<p><strong>Name:</strong> ${escapeHtml(name)}</p><p><strong>Email:</strong> ${escapeHtml(email)}</p><p>${escapeHtml(message).replace(/\r?\n/g, '<br>')}</p>`,
      }),
    });
    const body = await result.json();

    if (!result.ok) {
      console.error('Contact email provider returned an error:', result.status, body?.name || body?.statusCode);
      return response(502, { error: 'Your message could not be sent. Please try again later.' }, origin);
    }

    return response(200, { ok: true }, origin);
  } catch (error) {
    console.error('Contact email request failed:', error);
    return response(502, { error: 'Your message could not be sent. Please try again later.' }, origin);
  }
};
