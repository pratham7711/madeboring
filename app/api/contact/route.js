import nodemailer from 'nodemailer';

export async function POST(req) {
  let body;
  try {
    body = await req.json();
  } catch {
    return Response.json({ ok: false }, { status: 400 });
  }
  const name = String(body.name || '').trim().slice(0, 200);
  const email = String(body.email || '').trim().slice(0, 200);
  const message = String(body.message || '').trim().slice(0, 5000);
  if (body.company_website) return Response.json({ ok: true });
  if (!name || !message || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return Response.json({ ok: false, error: 'Fill in all three fields.' }, { status: 422 });
  }
  const user = process.env.CONTACT_SMTP_USER;
  const pass = process.env.CONTACT_SMTP_PASS;
  const to = process.env.CONTACT_TO || user;
  if (!user || !pass) {
    return Response.json({ ok: false, error: 'Mail is not configured.' }, { status: 503 });
  }
  try {
    const transport = nodemailer.createTransport({
      host: 'smtp.gmail.com',
      port: 465,
      secure: true,
      auth: { user, pass },
    });
    await transport.sendMail({
      from: `"madeboring.com" <${user}>`,
      to,
      replyTo: `"${name.replace(/"/g, '')}" <${email}>`,
      subject: `madeboring.com enquiry: ${name}`,
      text: `From: ${name} <${email}>\n\n${message}`,
    });
    return Response.json({ ok: true });
  } catch {
    return Response.json({ ok: false, error: 'Sending failed. Try again in a minute.' }, { status: 502 });
  }
}
