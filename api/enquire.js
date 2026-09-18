/**
 * CoverStar Kids Parties - Serverless Email Handler (Resend API)
 * Endpoint: /api/enquire
 * Dispatches availability enquiries to graham.m.222@gmail.com & bookings@coverstarexperiences.co.uk
 */

export default async function handler(req, res) {
  // Enforce POST method
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    return res.status(405).json({ error: `Method ${req.method} Not Allowed` });
  }

  try {
    const {
      parentName,
      email,
      phone,
      prefDate,
      childAge,
      groupSize,
      packageSelect,
      extraNotes
    } = req.body || {};

    // Validate required fields
    if (!parentName || !email || !phone || !prefDate) {
      return res.status(400).json({
        error: 'Missing required fields: parentName, email, phone, and prefDate are required.'
      });
    }

    const apiKey = process.env.RESEND_API_KEY;

    // Package Label Mapping
    const packageLabels = {
      gold: 'Gold Popstar Party (£199)',
      platinum: 'Platinum Popstar Party (£280)',
      ultimate: 'Ultimate Popstar Party (£380)',
      unsure: 'Not sure yet / Needs advice'
    };
    const packageText = packageLabels[packageSelect] || packageSelect || 'Not specified';

    // Format HTML Email Template
    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="utf-8">
        <title>New Party Enquiry</title>
      </head>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #1E293B; background-color: #F8FAFC; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #FFFFFF; border-radius: 12px; border: 2px solid #E2E8F0; padding: 28px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
          
          <!-- Banner Header -->
          <div style="background-color: #03113B; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 24px;">
            <h2 style="color: #FF2D55; margin: 0; font-size: 22px;">🎉 New Party Availability Enquiry</h2>
            <p style="color: #FFFFFF; margin: 4px 0 0 0; font-size: 14px;">CoverStar Kids Parties Liverpool</p>
          </div>

          <p style="font-size: 16px;">You have received a new date availability enquiry via the website:</p>

          <!-- Details Table -->
          <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px;">
            <tr style="border-bottom: 1px solid #E2E8F0;">
              <td style="padding: 10px 0; font-weight: bold; width: 40%; color: #475569;">Parent / Carer Name:</td>
              <td style="padding: 10px 0; color: #0F172A;">${escapeHtml(parentName)}</td>
            </tr>
            <tr style="border-bottom: 1px solid #E2E8F0;">
              <td style="padding: 10px 0; font-weight: bold; color: #475569;">Email Address:</td>
              <td style="padding: 10px 0;"><a href="mailto:${escapeHtml(email)}" style="color: #FF2D55; font-weight: bold;">${escapeHtml(email)}</a></td>
            </tr>
            <tr style="border-bottom: 1px solid #E2E8F0;">
              <td style="padding: 10px 0; font-weight: bold; color: #475569;">UK Phone Number:</td>
              <td style="padding: 10px 0;"><a href="tel:${escapeHtml(phone)}" style="color: #03113B; font-weight: bold;">${escapeHtml(phone)}</a></td>
            </tr>
            <tr style="border-bottom: 1px solid #E2E8F0;">
              <td style="padding: 10px 0; font-weight: bold; color: #475569;">Preferred Party Date:</td>
              <td style="padding: 10px 0; font-weight: bold; color: #03113B;">${escapeHtml(prefDate)}</td>
            </tr>
            <tr style="border-bottom: 1px solid #E2E8F0;">
              <td style="padding: 10px 0; font-weight: bold; color: #475569;">Child's Turning Age:</td>
              <td style="padding: 10px 0;">${escapeHtml(childAge || 'Not specified')}</td>
            </tr>
            <tr style="border-bottom: 1px solid #E2E8F0;">
              <td style="padding: 10px 0; font-weight: bold; color: #475569;">Estimated Group Size:</td>
              <td style="padding: 10px 0;">${escapeHtml(groupSize ? groupSize + ' guests' : 'Not specified')}</td>
            </tr>
            <tr style="border-bottom: 1px solid #E2E8F0;">
              <td style="padding: 10px 0; font-weight: bold; color: #475569;">Package Interest:</td>
              <td style="padding: 10px 0; font-weight: bold; color: #FF2D55;">${escapeHtml(packageText)}</td>
            </tr>
          </table>

          <!-- Special Notes Box -->
          <div style="background-color: #F1F5F9; padding: 16px; border-radius: 8px; border-left: 4px solid #FF2D55; margin-bottom: 24px;">
            <h4 style="margin: 0 0 8px 0; color: #03113B;">Special Requests / Message Notes:</h4>
            <p style="margin: 0; white-space: pre-wrap; font-size: 14px; color: #334155;">${escapeHtml(extraNotes || 'No extra notes provided.')}</p>
          </div>

          <!-- Footer Microcopy -->
          <div style="font-size: 13px; color: #64748B; border-top: 1px solid #E2E8F0; padding-top: 16px; text-align: center;">
            <p style="margin: 0;">💡 <strong>Quick Action:</strong> Click <em>Reply</em> in your email client to respond directly to ${escapeHtml(parentName)} at ${escapeHtml(email)}.</p>
          </div>

        </div>
      </body>
      </html>
    `;

    // If Resend API key is not configured yet (e.g. initial deployment check)
    if (!apiKey) {
      console.warn('RESEND_API_KEY environment variable is missing.');
      return res.status(200).json({
        success: true,
        warning: 'Resend API Key is unconfigured on the server environment. Please set RESEND_API_KEY.'
      });
    }

    // Call Resend API to dispatch email
    const fromEmail = process.env.RESEND_FROM_EMAIL || 'CoverStar Kids Parties <onboarding@resend.dev>';
    
    // Resend test domain (onboarding@resend.dev) only allows sending to the account owner (graham.m.222@gmail.com).
    // If a custom verified domain (RESEND_FROM_EMAIL) is set, send to both recipients.
    const recipients = process.env.RESEND_FROM_EMAIL
      ? ['graham.m.222@gmail.com', 'bookings@coverstarexperiences.co.uk']
      : ['graham.m.222@gmail.com'];


    const resendResponse = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from: fromEmail,
        to: recipients,
        reply_to: email,
        subject: `🎉 New Party Availability Enquiry - ${parentName} (${prefDate})`,
        html: htmlContent
      })
    });

    const resendData = await resendResponse.json();

    if (!resendResponse.ok) {
      console.error('Resend API Error:', resendData);
      return res.status(500).json({
        error: 'Failed to dispatch email via Resend',
        details: resendData
      });
    }

    return res.status(200).json({
      success: true,
      data: resendData
    });

  } catch (err) {
    console.error('Enquiry handler server error:', err);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str).replace(/[&<>"']/g, match => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  }[match]));
}
