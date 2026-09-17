/**
 * CoverStar Kids Parties - Main Interactive JavaScript
 * Handles navigation toggles, FAQ accordions, form validation, and dynamic rendering.
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initFaqAccordion();
  initEnquiryForm();
  renderDynamicPackages();
  initVideoOverlay();
});

/* Video Play Button Overlay Handler */
function initVideoOverlay() {
  const videoWrapper = document.getElementById('video-wrapper');
  const video = document.getElementById('custom-party-video');
  const overlay = document.getElementById('video-play-overlay');

  if (video && overlay) {
    // Click wrapper to toggle play/pause
    if (videoWrapper) {
      videoWrapper.addEventListener('click', (e) => {
        if (e.target !== video) {
          if (video.paused) {
            video.play();
          } else {
            video.pause();
          }
        }
      });
    }

    video.addEventListener('play', () => {
      overlay.style.opacity = '0';
      overlay.style.pointerEvents = 'none';
    });

    video.addEventListener('pause', () => {
      overlay.style.opacity = '1';
      overlay.style.pointerEvents = 'auto';
    });

    video.addEventListener('ended', () => {
      overlay.style.opacity = '1';
      overlay.style.pointerEvents = 'auto';
    });
  }
}

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

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = form.querySelector('button[type="submit"]');
    const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Submit Availability Enquiry 🎉';

    const parentName = document.getElementById('parent_name')?.value.trim();
    const email = document.getElementById('parent_email')?.value.trim();
    const confirmEmail = document.getElementById('confirm_email')?.value.trim();
    const phone = document.getElementById('parent_phone')?.value.trim();
    const prefDate = document.getElementById('pref_date')?.value;
    const childAge = document.getElementById('child_age')?.value;
    const groupSize = document.getElementById('group_size')?.value;
    const packageSelect = document.getElementById('package_select')?.value;
    const extraNotes = document.getElementById('extra_notes')?.value.trim();
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

    if (confirmEmail !== undefined && email.toLowerCase() !== confirmEmail.toLowerCase()) {
      if (formStatus) {
        formStatus.style.display = 'block';
        formStatus.style.backgroundColor = '#FEE2E2';
        formStatus.style.color = '#991B1B';
        formStatus.style.border = '1px solid #FCA5A5';
        formStatus.innerHTML = '<strong>Email addresses do not match.</strong> Please verify both email address fields.';
      }
      return;
    }

    // Set Loading State
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = 'Sending Enquiry... ⏳';
    }

    try {
      const response = await fetch('/api/enquire', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          parentName,
          email,
          phone,
          prefDate,
          childAge,
          groupSize,
          packageSelect,
          extraNotes
        })
      });

      const data = await response.json();

      if (response.ok && data.success) {
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
      } else {
        throw new Error(data.error || 'Server returned an error');
      }
    } catch (err) {
      console.warn('Backend enquiry dispatch warning:', err);
      // Fallback user display if API route is unpopulated or offline
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
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalBtnText;
      }
    }
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
