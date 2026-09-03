---
name: coverstar-kids-parties-pages
description: Generates high-converting, local SEO landing pages and HTML templates for Coverstar Kids Parties in Liverpool and surrounding regions.
---

# Coverstar Kids Parties - Page Creator Skill

## Overview
This skill defines the technical standards, design system tokens, structured data schemas, and CRO layout requirements for generating local SEO landing pages for **Coverstar Kids Parties** (domain: `coverstarkidsparties.co.uk`, parent company: *Coverstar Experiences*).

---

## Brand Identity & E-E-A-T Profile

* **Trading Name**: Coverstar Kids Parties
* **Parent Brand**: Coverstar Experiences
* **Venue Location**: Prohibition Recording Studios, Liverpool City Centre, Merseyside
* **Phone Number**: 0800 689 7827
* **Primary URL**: https://coverstarkidsparties.co.uk
* **Logo URL**: https://www.coverstarexperiences.co.uk/wp-content/uploads/2016/08/CoverStar-Experiences-Master-Logo-Centered-150x150.jpg
* **Favicon URL**: https://www.coverstarexperiences.co.uk/wp-content/uploads/2016/08/cropped-CoverStar-Experiences-Master-Logo-Centered-100x100.jpg
* **Accreditations**: 10-Time TripAdvisor Travellers' Choice Award Winner (2014, 2015, 2016, 2018, 2019, 2021, 2022, 2023, 2024, 2025).

---

## Design System Tokens (CSS Custom Properties)

Every page template must embed or reference the following CSS design tokens:

```css
:root {
  /* Brand Colours */
  --color-primary: #DCC700;        /* Gold / Bright Yellow */
  --color-secondary: #03113B;      /* Deep Navy Blue */
  --color-accent: #CBB000;         /* Deep Gold Accent */
  --color-bg: #FFFFFF;             /* Crisp Light Background */
  --color-text-primary: #03113B;   /* Deep Navy Text */
  --color-text-muted: #556285;     /* Soft Muted Text */
  --color-link: #CBB000;           /* Interactive Gold Links */
  --color-card-bg: #F8F9FD;        /* Soft Cool Gray Card Fill */
  --color-border: #E2E8F0;         /* Subtle Border Divider */

  /* Typography */
  --font-heading: 'Abel', sans-serif;
  --font-display: 'Cabin Sketch', cursive;
  --font-body: 'Open Sans Condensed', sans-serif;
  --font-accent: 'Quicksand', 'Montserrat', sans-serif;

  /* Font Sizes */
  --fs-h1: 48px;
  --fs-h2: 42px;
  --fs-h3: 28px;
  --fs-body: 21px;
  --fs-small: 16px;

  /* Layout & Spacing */
  --spacing-unit: 4px;
  --border-radius: 3px;
  --max-width: 1200px;
}
```

---

## Structured Data Schemas (JSON-LD)

Each generated page must contain a valid `application/ld+json` script block containing `LocalBusiness`, `Service`, and `FAQPage` schemas:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "EntertainmentBusiness",
      "@id": "https://coverstarkidsparties.co.uk/#organization",
      "name": "Coverstar Kids Parties",
      "legalName": "CoverStar Experiences",
      "url": "https://coverstarkidsparties.co.uk",
      "logo": "https://www.coverstarexperiences.co.uk/wp-content/uploads/2016/08/CoverStar-Experiences-Master-Logo-Centered-150x150.jpg",
      "telephone": "0800 689 7827",
      "address": {
        "@type": "PostalAddress",
        "addressLocality": "Liverpool",
        "addressRegion": "Merseyside",
        "addressCountry": "GB"
      },
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5.0",
        "reviewCount": "250"
      },
      "priceRange": "£199 - £380"
    },
    {
      "@type": "Service",
      "name": "Children's Recording Studio Birthday Parties",
      "provider": {
        "@id": "https://coverstarkidsparties.co.uk/#organization"
      },
      "areaServed": {
        "@type": "AdministrativeArea",
        "name": "Liverpool and Merseyside"
      },
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "name": "Kids Party Packages",
        "itemListElement": [
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "Service",
              "name": "Gold Popstar Party",
              "description": "1.5 hours studio time, 1 song, sound engineer, personalised vinyl style CD"
            },
            "price": "199.00",
            "priceCurrency": "GBP"
          },
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "Service",
              "name": "Platinum Popstar Party",
              "description": "2 hours studio time, 2 songs, sound engineer, gold personalised vinyl style CD"
            },
            "price": "280.00",
            "priceCurrency": "GBP"
          },
          {
            "@type": "Offer",
            "itemOffered": {
              "@type": "Service",
              "name": "Ultimate Popstar Party",
              "description": "2 hours studio time, 2 songs, party host, photographer, festival make-up"
            },
            "price": "380.00",
            "priceCurrency": "GBP"
          }
        ]
      }
    }
  ]
}
```

---

## Page Layout & Section Hierarchy (CRO Blueprint)

1. **Header & Top Announcement**:
   - Contact phone (`0800 689 7827`), Enquiry Button, Liverpool City Centre venue location tag.
2. **Hero Section (High Energy)**:
   - Primary Headline (H1, 48px): High impact, location-matched title (e.g. *The Ultimate Kids Recording Studio Parties in Liverpool*).
   - Subtitle: Mentioning popstar experience, 10-time TripAdvisor award winner, and real studio recording.
   - Direct CTA Buttons: [ENQUIRE NOW] and [SEE PACKAGES].
   - Key Feature Pills: 1.5+ Hours Studio Time, City Centre Location, Any Group Size, 10+ Years Experience.
3. **Trust & Social Proof Bar**:
   - TripAdvisor Travellers' Choice Winner Badges (2014-2025).
   - 5-Star Parent Rating highlights.
4. **Intro & Value Proposition**:
   - "No Ordinary Kids Party": How kids record in Prohibition Recording Studios without needing prior singing skills.
   - Highlights: Soundproof vocal booth, digital mixing desk, lyric screen, personalised vinyl-style CDs.
5. **Party Packages & Pricing Grid**:
   - **Gold Popstar Party (£199)**: 8 guests included, £25/extra guest, 1 song, 1.5h studio time, sound engineer, 1 VIP CD, digital download.
   - **Platinum Popstar Party (£280)**: 8 guests included, £35/extra guest, 2 songs, 2h studio time, CDs for everyone, 1 Gold VIP CD, digital download.
   - **Ultimate Popstar Party (£380)**: 10 guests included, £38/extra guest, 2 songs, 2h studio time, Party Host, Edited Photos, Festival Make-up.
6. **The 3-Step Popstar Experience**:
   - Step 1: Rehearsal Time (Vocal warm-ups & lyric check with engineer).
   - Step 2: Studio Time (Booth recording with headphones & screens).
   - Step 3: Fame Time (Cake, photos, receiving personalized vinyl-style CDs).
7. **SEO Prose & Location Context**:
   - Unique, highly tailored content focusing on the specific target location (e.g. Liverpool City Centre, Wirral, Sefton, St Helens, Knowsley, Cheshire).
   - Addressing Ideal Customer Avatar (ICA) pain points: stress-free hosting, DBS security, indoor weather-proof fun, lifetime memories.
8. **Real Customer Reviews**:
   - Verified parent testimonials from TripAdvisor highlighting staff members (Matt, Holly, Ruby).
9. **Frequently Asked Questions (FAQ Accordion)**:
   - Detailed answers covering arrival, group sizes, song choices, kitchen/catering facilities, parents' attendance.
10. **Final High-Converting CTA Banner**:
    - Urgency drive to lock in party dates in advance with booking link and direct phone number.

---

## Copywriting & Content Rules

1. **Language & Grammar**: Must use UK English spelling exclusively (e.g., *colour*, *customised*, *centre*, *favourite*).
2. **Strict Punctuation Rule**: NEVER use em dashes (the character —). Use colons, hyphens, or parentheses instead.
3. **Mobile Readability**: Paragraphs must not exceed 3 lines on mobile displays.
4. **Duplicate Content Prevention**:
   - Every location-targeted landing page must have 100% unique prose.
   - Do NOT perform simple location search-and-replace swaps.
   - Customise local landmarks, travel access (e.g. Lime Street station, Merseyrail access for Wirral parents), and location-specific intro hooks for each area.
