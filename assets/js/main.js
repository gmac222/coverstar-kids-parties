/**
 * CoverStar Kids Parties - Main Interactive JavaScript
 * Handles navigation toggles, FAQ accordions, form validation, and dynamic rendering.
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initFaqAccordion();
  initEnquiryForm();
  renderDynamicPackages();
});

/* Mobile Navigation Toggle */
function initMobileNav() {
  const toggleBtn = document.querySelector('.mobile-nav-toggle');
  const navMenu = document.querySelector('.nav-menu');

  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', () => {
      navMenu.classList.toggle('active');
      toggleBtn.setAttribute('aria-expanded', navMenu.classList.contains('active'));
    });
  }
}

/* FAQ Accordion Handler */
function initFaqAccordion() {
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question');
    if (questionBtn) {
      questionBtn.addEventListener('click', () => {
        const isOpen = item.classList.contains('open');

        // Close other accordion items
        faqItems.forEach(other => other.classList.remove('open'));

        if (!isOpen) {
          item.classList.add('open');
        }
      });
    }
  });
}

/* Enquiry Form Validation & Submission Handler */
function initEnquiryForm() {
  const form = document.getElementById('availability-form');
  const formStatus = document.getElementById('form-status-message');

  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const parentName = document.getElementById('parent_name')?.value.trim();
    const email = document.getElementById('parent_email')?.value.trim();
    const phone = document.getElementById('parent_phone')?.value.trim();
    const prefDate = document.getElementById('pref_date')?.value;
    const consent = document.getElementById('privacy_consent')?.checked;

    if (!parentName || !email || !phone || !prefDate || !consent) {
      if (formStatus) {
        formStatus.style.display = 'block';
        formStatus.style.backgroundColor = '#FEE2E2';
        formStatus.style.color = '#991B1B';
        formStatus.style.border = '1px solid #FCA5A5';
        formStatus.innerHTML = '<strong>Please complete all required fields</strong> including parent name, email, phone, preferred date, and privacy consent.';
      }
      return;
    }

    // Success response state
    if (formStatus) {
      formStatus.style.display = 'block';
      formStatus.style.backgroundColor = '#D1FAE5';
      formStatus.style.color = '#065F46';
      formStatus.style.border = '1px solid #6EE7B7';
      formStatus.innerHTML = `
        <h4 style="margin-bottom: 8px; color: #065F46;">Thank you, ${escapeHtml(parentName)}!</h4>
        <p style="margin-bottom: 8px;">Your date check for <strong>${escapeHtml(prefDate)}</strong> has been received by CoverStar Kids Parties.</p>
        <p style="margin-bottom: 0; font-size: 14px;">Please note: your date is not reserved yet. Our organising team will review studio availability and contact you shortly via <strong>${escapeHtml(phone)}</strong> or <strong>${escapeHtml(email)}</strong>. A £50 deposit is used to secure an agreed slot once details are confirmed.</p>
      `;
    }

    form.reset();
  });
}

/* Render Dynamic Package Cards if Container Exists */
function renderDynamicPackages() {
  const container = document.getElementById('dynamic-packages-container');
  if (!container || typeof COVERSTAR_DATA === 'undefined') return;

  container.innerHTML = COVERSTAR_DATA.packages.map(pkg => `
    <div class="package-card ${pkg.highlight ? 'highlight' : ''}">
      ${pkg.badgeText ? `<div class="card-top-tag">${pkg.badgeText}</div>` : ''}
      <h3 class="package-title">${pkg.name}</h3>
      <div class="package-price-row">
        <span class="price-main">£${pkg.price.toFixed(2)}</span>
      </div>
      <div class="package-guests-note">
        Set rate for up to ${pkg.guestsIncluded} guests. £${pkg.extraGuestPrice.toFixed(2)} per additional guest.
      </div>
      <ul class="package-checklist">
        ${pkg.features.map(feat => `<li>${feat}</li>`).join('')}
      </ul>
      <a href="/contact/#enquire" class="btn ${pkg.highlight ? '' : 'btn-outline-gold'} btn-full">
        Check Date For This Package
      </a>
    </div>
  `).join('');
}

/* Helper Utility function */
function escapeHtml(str) {
  return str.replace(/[&<>"']/g, match => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  }[match]));
}
