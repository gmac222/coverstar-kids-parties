#!/usr/bin/env python3
"""
Build the /blog/ section for coverstarkidsparties.co.uk.

Generates blog/index.html and one HTML file per post from a shared template so
the header, footer, tracking tags and schema stay identical to the rest of the
site. Run from the repository root:

    python3 scripts/build_blog.py

Business facts (prices, ages, address, deposit) are taken from the same values
held in assets/js/site-data.js. Update both if a fact changes.
"""

import html
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(ROOT, "blog")
SITE = "https://coverstarkidsparties.co.uk"
PUBLISHED = "2026-11-15"
AUTHOR = "CoverStar Kids Parties Team"

# ---------------------------------------------------------------------------
# Shared chrome (copied from about-coverstar/index.html, with Blog nav added)
# ---------------------------------------------------------------------------

HEAD = """<!DOCTYPE html>
<html lang="en-GB">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-ZZQCQ5P0JW"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());

    gtag('config', 'G-ZZQCQ5P0JW');
    gtag('config', 'AW-757671729');
  </script>

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{canonical}">
{extra_meta}    <link rel="icon" type="image/png" href="/assets/images/favicon.png">
  <link rel="shortcut icon" href="/favicon.ico">
  <link rel="apple-touch-icon" href="/assets/images/favicon.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Abel&family=Cabin+Sketch:wght@700&family=Inter:wght@400;500;600;700&family=Open+Sans+Condensed:wght@300;700&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="/assets/css/main.css">
{schema}</head>
<body>
"""

TOP_BAR_AND_HEADER = """
  <!-- Bright Yellow Top Bar -->
  <div class="top-endorsement-bar">
    <div class="top-bar-socials">
      <a href="https://www.facebook.com/CoverStar/" target="_blank" rel="noopener" aria-label="CoverStar Facebook Page" class="social-icon-link" title="Facebook">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
      </a>
      <a href="https://x.com/coverstar_exps" target="_blank" rel="noopener" aria-label="CoverStar X Twitter Page" class="social-icon-link" title="X (Twitter)">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
      </a>
      <a href="https://www.instagram.com/coverstar_exps/" target="_blank" rel="noopener" aria-label="CoverStar Instagram Page" class="social-icon-link" title="Instagram">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
      </a>
      <a href="https://www.pinterest.com/CoverStarExps/" target="_blank" rel="noopener" aria-label="CoverStar Pinterest Page" class="social-icon-link" title="Pinterest">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.372 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738.098.119.112.224.083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.631-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12 24c6.627 0 12-5.373 12-12 0-6.628-5.373-12-12-12z"/></svg>
      </a>
      <a href="https://www.youtube.com/user/CoverStarExperiences" target="_blank" rel="noopener" aria-label="CoverStar YouTube Channel" class="social-icon-link" title="YouTube">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
      </a>
      <a href="https://www.tripadvisor.co.uk/Attraction_Review-g186337-d3860194-Reviews-CoverStar_Experiences-Liverpool_Merseyside_England.html" target="_blank" rel="noopener" aria-label="CoverStar TripAdvisor Page" class="social-icon-link" title="TripAdvisor">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"/></svg>
      </a>
    </div>
    <div class="top-bar-phone">
      <a href="tel:08006897827" style="color: var(--color-secondary);">📞 0800 689 7827</a>
    </div>
  </div>

  <!-- White Site Header -->
  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="brand-block">
        <img src="/assets/images/coverstar-logo.jpg" alt="CoverStar Logo" class="brand-logo-img">
      </a>

      <nav>
        <ul class="nav-menu">
          <li><a href="/" class="nav-link">Home</a></li>
          <li><a href="/about-coverstar/" class="nav-link">About Us</a></li>
          <li><a href="/blog/" class="nav-link" style="color: var(--color-primary-dark);">Blog</a></li>
          <li><a href="/contact/" class="nav-link">Contact</a></li>
        </ul>
      </nav>

      <div style="display: flex; align-items: center; gap: 16px;">
        <a href="/contact/#enquire" class="btn" style="padding: 8px 18px; font-size: 15px;">Check Availability</a>
        <button class="mobile-nav-toggle" aria-label="Toggle navigation menu">☰</button>
      </div>
    </div>
  </header>
"""

FOOTER = """
    <!-- Mobile Sticky Bar -->
  <div class="mobile-sticky-bar">
    <div class="mobile-sticky-inner">
      <a href="/contact/#enquire" class="btn btn-pink">Enquire For Dates 🎉</a>
      <a href="/#packages" class="btn btn-white-navy">See Packages 📀</a>
    </div>
  </div>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <a href="/" style="display: inline-block; margin-bottom: 14px;">
            <img src="/assets/images/coverstar-logo.jpg" alt="CoverStar Experiences Logo" style="height: 64px; width: auto; border-radius: 8px; border: 2px solid #FFFFFF; background-color: #FFFFFF;">
          </a>
          <h4 style="margin-top: 4px;">CoverStar Kids Parties</h4>
          <p style="font-size: 13px;">A specialist children's popstar party venue operated by <strong>CoverStar Experiences</strong>.</p>
          <p style="font-size: 13px; margin-top: 8px;">Prohibition Recording Studios<br>24a Arrad Street, Georgian Quarter<br>Liverpool City Centre, L7 7BP</p>
        </div>

        <div class="footer-col">
          <h4>Navigation</h4>
          <ul class="footer-links">
            <li><a href="/">Home</a></li>
            <li><a href="/about-coverstar/">About CoverStar</a></li>
            <li><a href="/blog/">Party Planning Blog</a></li>
            <li><a href="/contact/">Check Availability &amp; Contact</a></li>
          </ul>
        </div>

        <div class="footer-col">
          <h4>Opening Hours 🕒</h4>
          <p style="font-size: 13px; line-height: 1.6; color: #A0AEC0;">
            <strong>Mon - Fri:</strong> 9:00am - 9:00pm<br>
            <strong>Saturday:</strong> 9:00am - 9:00pm<br>
            <strong>Sunday:</strong> 10:00am - 6:00pm
          </p>
        </div>

        <div class="footer-col">
          <h4>Legal &amp; Support</h4>
          <ul class="footer-links">
            <li><a href="/legal/privacy-policy.html">Privacy Policy</a></li>
            <li><a href="/legal/cookie-policy.html">Cookie Policy</a></li>
            <li><a href="/legal/terms-and-conditions.html">Terms &amp; Conditions</a></li>
            <li><a href="/legal/accessibility.html">Accessibility Statement</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom">
        <p>&copy; 2026 CoverStar Kids Parties. Operated by CoverStar Experiences. All Rights Reserved.</p>
      </div>
    </div>
  </footer>

  <script src="/assets/js/site-data.js"></script>
  <script src="/assets/js/main.js"></script>
</body>
</html>
"""

CTA_BLOCK = """
        <div class="article-cta">
          <h2>Thinking About a Recording Studio Party?</h2>
          <p>Check your date with our friendly Liverpool team. Packages start at £199 for up to 8 children, and a £50 deposit secures your slot.</p>
          <div class="article-cta-buttons">
            <a href="/contact/#enquire" class="btn btn-pink">Check Your Party Date 🎉</a>
            <a href="/#packages" class="btn btn-white-navy">View Packages &amp; Prices 📀</a>
          </div>
        </div>
"""

# ---------------------------------------------------------------------------
# Posts
# ---------------------------------------------------------------------------

POSTS = [
    {
        "slug": "how-to-plan-kids-birthday-party-liverpool",
        "tag": "Planning",
        "title": "How to Plan a Kids' Birthday Party in Liverpool",
        "meta_title": "How to Plan a Kids' Birthday Party in Liverpool | Step-by-Step Guide",
        "description": "A practical, week-by-week guide to planning a children's birthday party in Liverpool: picking a date, choosing a venue, guest lists, food, budget and day-of logistics.",
        "image": "/assets/images/studio-party-kids-enhanced.jpg",
        "image_alt": "Group of children celebrating a birthday party inside a Liverpool recording studio",
        "excerpt": "From picking a weekend that is not already booked out to knowing where to park in the city centre, here is the planning timeline Liverpool parents actually use.",
        "lead": "Planning a children's party is one of those jobs that looks small until you start it. The good news is that it breaks down into a handful of decisions, and if you make them in the right order the rest falls into place. This guide walks through the timeline we see work best for Liverpool families, with the local details that national party guides tend to miss.",
        "body": """
<h2>Start With Three Decisions</h2>
<p>Almost everything else depends on these, so settle them first:</p>
<ol>
  <li><strong>Who is coming.</strong> A rough number is enough for now. Whole class, half a dozen close friends, or family plus a few mates. The number drives the venue, the budget and the format.</li>
  <li><strong>Roughly when.</strong> The actual birthday, the nearest weekend, or a date in the school holidays. Liverpool schools do not all share identical term dates, so if guests come from more than one school, check both calendars before you print invitations.</li>
  <li><strong>At home or out.</strong> A home party is cheaper on paper but costs you a full day of setting up, hosting and clearing. A venue or activity party costs more per child but comes with staff, structure and someone else doing the tidying.</li>
</ol>

<h2>The Planning Timeline</h2>
<div class="article-table-scroll">
<table>
  <thead>
    <tr><th>When</th><th>What to do</th></tr>
  </thead>
  <tbody>
    <tr><td><strong>6 to 8 weeks before</strong></td><td>Shortlist venues and check availability. Popular Saturday afternoon slots across Liverpool go quickly, especially in the run-up to Christmas and the May and October half terms. Pay the deposit to hold your date.</td></tr>
    <tr><td><strong>4 to 5 weeks before</strong></td><td>Confirm the guest list with your child. Send invitations with a clear RSVP date about two weeks before the party.</td></tr>
    <tr><td><strong>3 weeks before</strong></td><td>Order or plan the cake. Decide on food: bring your own, order in, or use what the venue provides. Ask parents about allergies on the RSVP.</td></tr>
    <tr><td><strong>1 to 2 weeks before</strong></td><td>Chase RSVPs. Confirm final numbers with the venue and check what time you can arrive to set up. Buy or make party bags if you are doing them.</td></tr>
    <tr><td><strong>2 days before</strong></td><td>Pack a party box: candles, lighter, knife, napkins, plates, a bin bag, phone charger, wet wipes, spare plasters. Write the address and phone number of the venue on the invitation reminder you send to parents.</td></tr>
    <tr><td><strong>On the day</strong></td><td>Arrive early, brief whoever is helping you, and give yourself one job: enjoy it. Delegate photos to another adult.</td></tr>
  </tbody>
</table>
</div>

<h2>Choosing a Liverpool Venue</h2>
<p>Liverpool has a wide spread of party options, from soft play centres and trampoline parks on the retail parks to city centre experiences you cannot get elsewhere. When you compare them, ask the same questions of each:</p>
<ul>
  <li>Is the price per child or a flat package? What is the minimum and maximum group size?</li>
  <li>How long is the slot, and does it include time for food and cake?</li>
  <li>Is the space private or shared with the public?</li>
  <li>What do the children take home? A party bag of sweets, or something they will keep?</li>
  <li>Where do parents wait, and how many adults need to stay?</li>
</ul>
<p>At our own <a href="/">recording studio parties</a> the answers are: flat package pricing from £199 for 8 children, slots of 1.5 or 2 hours including a party room for food, a private studio, a recorded song on a vinyl-style CD plus a download, and a parents' lounge with a bar. At least one parent or guardian stays throughout. If you are weighing up other kinds of venue, our guide to <a href="/blog/kids-party-ideas-liverpool-beyond-soft-play.html">party ideas beyond soft play</a> runs through the main categories.</p>

<h2>Getting There: City Centre Logistics</h2>
<p>If you book anywhere in the city centre, give parents the practical details in advance so nobody arrives flustered.</p>
<ul>
  <li><strong>Parking.</strong> Our studio is at 24a Arrad Street in the Georgian Quarter (L7 7BP). On-street parking on Hope Street and the Metropolitan Cathedral car park are both about a two-minute walk away. Weekend parking in the Georgian Quarter is usually easier than around Liverpool ONE.</li>
  <li><strong>Trains.</strong> Liverpool Lime Street and Liverpool Central are both a 10 to 15 minute walk from the Georgian Quarter, which suits families coming in from the Wirral, Southport or Ormskirk on Merseyrail.</li>
  <li><strong>Drop-off.</strong> Agree a single drop-off and collection point with parents. Children spilling out across a city pavement is the most stressful ten minutes of any party.</li>
</ul>

<h2>Food Without the Fuss</h2>
<p>Children at a party eat less than you think and far more sugar than you plan. A simple spread works: a savoury option, fruit, crisps, and the cake. If your venue lets you bring your own food, as we do, that keeps costs down and means you can cater for allergies yourself. Many of our parents order pizza to arrive while the CDs are being printed; tell the venue in advance so it lands at the right moment and does not interrupt the activity.</p>

<h2>Party Bags: Worth It?</h2>
<p>Party bags are the most-skipped item on modern party lists and few children notice. If the party itself produces a keepsake, such as a craft they made, a photo, or in our case a recording of their song, that does the job of the party bag with far less plastic. If you do want bags, one decent item beats five cheap ones.</p>

<h2>A Few Things Experienced Parents Do</h2>
<ul>
  <li>Keep the party to two hours. It is long enough to feel like an event and short enough that nobody melts down.</li>
  <li>Invite an even number if the activity involves pairing up.</li>
  <li>Put a second adult in charge of the birthday child's gifts and cards so they do not get separated.</li>
  <li>Ask the venue when the best moment for cake is. Doing it at the natural break in the activity keeps the energy up.</li>
  <li>Take one group photo before anything starts, while everyone still looks tidy.</li>
</ul>

<div class="article-callout">
  <h3>Planning a party for an older child?</h3>
  <p>The sweet spot changes with age. See our ideas for <a href="/blog/birthday-party-ideas-8-to-12-year-olds.html">8 to 12 year olds</a> and <a href="/blog/teen-birthday-party-ideas-liverpool.html">teenagers in Liverpool</a>.</p>
</div>
""",
    },
    {
        "slug": "how-much-does-kids-party-cost-liverpool",
        "tag": "Budget",
        "title": "How Much Does a Kids' Party Cost in Liverpool?",
        "meta_title": "How Much Does a Kids' Party Cost in Liverpool? 2026 Price Guide",
        "description": "Honest breakdown of what a children's birthday party costs in Liverpool, from home parties to venue packages, with per-child maths, hidden extras and ways to keep the bill down.",
        "image": "/assets/images/cd-vinyl-keepsake.jpg",
        "image_alt": "Personalised gold vinyl-style CD keepsake from a CoverStar kids party",
        "excerpt": "Per head or flat fee? What is actually included? We break down the real cost of a children's party in Liverpool and show how to compare venues fairly.",
        "lead": "Ask ten Liverpool parents what they spent on their child's last party and you will get answers from under £100 to well over £500. The spread is not because some parents are extravagant. It is because \"a party\" covers everything from cake and games in the living room to a private hire with entertainers and catering. This guide sets out the cost components so you can budget properly and compare venues like for like.",
        "body": """
<h2>The Six Things You Are Paying For</h2>
<ol>
  <li><strong>Venue or activity.</strong> The biggest line. Charged either per child or as a flat package with a set number of places.</li>
  <li><strong>Food and drink.</strong> Included in some packages, bring-your-own at others, and a separate catering charge at some.</li>
  <li><strong>Cake.</strong> Supermarket cakes start cheap; bespoke bakery cakes in Liverpool can run to a meaningful chunk of the total budget.</li>
  <li><strong>Invitations and decorations.</strong> Easy to spend nothing on, easy to spend a lot.</li>
  <li><strong>Party bags.</strong> Optional, and increasingly skipped.</li>
  <li><strong>Extras.</strong> Entertainers, photographers, face painting, additional guests over the package allowance, and the deposit timing.</li>
</ol>

<h2>Per Child or Flat Fee? Do the Maths</h2>
<p>Activity venues such as soft play centres and trampoline parks usually price per child with a minimum number. Experience venues often price as a package for a set group, with a per-head charge for extra guests. Neither is inherently cheaper. What matters is the cost at <em>your</em> group size.</p>
<p>Here is how our own packages work out per child at the included group size:</p>
<div class="article-table-scroll">
<table>
  <thead>
    <tr><th>Package</th><th>Price</th><th>Children included</th><th>Cost per child</th><th>Extra guests</th></tr>
  </thead>
  <tbody>
    <tr><td>Gold Popstar Party</td><td>£199</td><td>8</td><td>About £25</td><td>£25 each</td></tr>
    <tr><td>Platinum Popstar Party</td><td>£280</td><td>8</td><td>£35</td><td>£35 each</td></tr>
    <tr><td>Ultimate Popstar Party</td><td>£380</td><td>10</td><td>£38</td><td>£38 each</td></tr>
  </tbody>
</table>
</div>
<p>Each package includes studio time with a professional sound engineer, backing tracks and lyric screen, a recorded song (two songs on Platinum and Ultimate), vinyl-style CDs and a digital download. Ultimate adds a dedicated party host, professionally edited photos and festival-style make-up and props. Full details are on our <a href="/#packages">packages section</a>.</p>
<p>When you compare any venue, add up the <em>total</em> for your actual number of children, including anything you must buy separately, before you look at the headline figure.</p>

<h2>What a Home Party Really Costs</h2>
<p>A home party avoids the venue fee but rarely comes in at zero. Once you add food for children and the parents who linger, decorations, a cake, games prizes, party bags and possibly a hired entertainer or bouncy castle, a home party for ten children can comfortably reach the price of a mid-range venue package. The true cost is your time: a day of preparation, three hours of hosting, and an evening of clearing up.</p>

<h2>Hidden Costs to Ask About</h2>
<ul>
  <li><strong>Minimum numbers.</strong> Per-child venues often charge for a minimum of 8 or 10 even if fewer come.</li>
  <li><strong>Adult food and drink.</strong> If parents stay, do they eat? Some venues charge for adult places.</li>
  <li><strong>Socks, wristbands or safety gear</strong> at trampoline and soft play venues.</li>
  <li><strong>Room hire time.</strong> Is the party room included, or an add-on after the activity?</li>
  <li><strong>Deposit and balance terms.</strong> Ours is a £50 deposit to hold the slot. Ask when the balance is due and what the cancellation terms are.</li>
  <li><strong>Peak pricing.</strong> Some venues charge more on Saturdays or in school holidays. Ours does not vary by day.</li>
</ul>

<h2>Where the Money Shows</h2>
<p>Spend where it changes the child's experience and save where it does not.</p>
<ul>
  <li><strong>Spend on the activity.</strong> It is what they remember and talk about at school on Monday.</li>
  <li><strong>Save on decorations.</strong> A banner and balloons are plenty. Nobody has ever remembered a tablecloth.</li>
  <li><strong>Save on party bags</strong> if the party produces its own keepsake. Every child at our parties leaves with the recording of the song they made together, which is the party bag.</li>
  <li><strong>Be realistic about numbers.</strong> Going from 8 to 14 guests nearly doubles most budgets. Smaller groups also suit children over about 8 far better, as we explain in our <a href="/blog/birthday-party-ideas-8-to-12-year-olds.html">guide for 8 to 12 year olds</a>.</li>
</ul>

<h2>Ways to Keep the Bill Down</h2>
<ul>
  <li>Choose a venue that lets you bring your own food and cake, and shop for it yourself. We do, and parents often save a significant amount this way.</li>
  <li>Book a weekday or Sunday slot if your venue prices those lower.</li>
  <li>Share the party with a friend who has a birthday the same month and split a package.</li>
  <li>Send digital invitations.</li>
  <li>Ask whether the venue includes photos. Ours do on the Ultimate package, which can replace a separate photographer.</li>
</ul>

<div class="article-callout">
  <h3>A sample budget: recording studio party for 8</h3>
  <p>Gold Popstar Party £199, plus a supermarket cake, pizzas delivered to the studio, drinks and snacks brought from home. Most families doing it this way land somewhere in the mid £200s all in, with every child taking home a CD and download of their recording. Want exact numbers for your group size? <a href="/contact/#enquire">Ask us for a quote</a>.</p>
</div>
""",
    },
    {
        "slug": "kids-party-ideas-liverpool-beyond-soft-play",
        "tag": "Ideas",
        "title": "Kids' Party Ideas in Liverpool Beyond Soft Play",
        "meta_title": "Kids' Party Ideas in Liverpool Beyond Soft Play | CoverStar Kids Parties",
        "description": "Bored of the same soft play and trampoline parties? Here are children's party ideas across Liverpool, from recording studios to museums, beaches and stadium tours, sorted by age.",
        "image": "/assets/images/popstar-party-singing.jpg",
        "image_alt": "Children singing together into a studio microphone at a Liverpool pop star party",
        "excerpt": "Soft play has its place, but by age seven most children have been to the same three venues. Here are the Liverpool alternatives parents tell us they wish they had found sooner.",
        "lead": "There is nothing wrong with soft play. For toddlers and infants it is close to perfect. The problem is that by Year 2 or 3 most children in Liverpool have been to every soft play centre and trampoline park within half an hour of home, often several times each. If you are hunting for something different, Liverpool has more options than its retail parks suggest.",
        "body": """
<h2>Creative and Performance Parties</h2>
<h3>Record a song in a real studio</h3>
<p>This is what we do, so we will declare the bias up front. A group of children rehearse and record a pop song with a professional sound engineer in a working Liverpool recording studio, with a lyric screen and backing track so nobody needs to be a confident singer. The birthday child can do solo takes, everyone sings the chorus together, and each child leaves with the recording on a vinyl-style CD and a download. It suits ages 7 to 16, works equally well for mixed groups, and the recording is something families genuinely keep. <a href="/">See how a CoverStar party works</a>.</p>
<h3>Pottery painting and craft studios</h3>
<p>Liverpool has several paint-your-own-pottery and craft studios that host parties. Quieter than an activity party, good for children who prefer making to running, and everyone takes home what they made. Allow for a return trip or postage if pieces need glazing and firing.</p>
<h3>Theatre and drama workshops</h3>
<p>Several Liverpool drama schools and theatres run party workshops where a practitioner leads games and a mini performance. A good fit for children who love dressing up and being the centre of attention.</p>

<h2>Out and About in Liverpool</h2>
<h3>Museums on the waterfront</h3>
<p>The World Museum, Museum of Liverpool and the Maritime Museum are free to enter, which makes a self-organised museum trail party one of the cheapest options in the city. Set a scavenger hunt, finish with cake at a nearby café. Best for smaller, well-behaved groups with plenty of adults.</p>
<h3>Beaches and parks</h3>
<p>Crosby beach with the Antony Gormley iron men, Formby's dunes and pinewoods, and Sefton Park with its Palm House are all free and a short drive or Merseyrail trip from the city. Great for summer birthdays with a picnic and games. Have a wet-weather backup.</p>
<h3>Stadium tours</h3>
<p>For a football-mad child, a stadium tour at Anfield is a memorable birthday treat for a small group, especially combined with lunch afterwards. Check minimum ages and group terms with the club.</p>
<h3>The Mersey Ferry and the Beatles</h3>
<p>A ferry across the Mersey followed by the Beatles Story at the Albert Dock is a proper Liverpool day out for older children who are into music. If your child is a budding musician, pair the Beatles theme with recording a Beatles song at a studio party and you have a theme that runs through the whole day.</p>

<h2>Active Alternatives to Soft Play</h2>
<ul>
  <li><strong>Climbing and bouldering centres</strong> run children's parties with instructors. Good for ages 6 and up with a competitive streak.</li>
  <li><strong>Swimming parties</strong> at council leisure centres are often good value and include a party room. Check lifeguard ratios and adult requirements.</li>
  <li><strong>Football and multi-sport parties</strong> on 3G pitches with a coach. Simple, cheap per head, and parents can watch from the sideline.</li>
  <li><strong>Bowling and arcades</strong> remain a reliable crowd-pleaser from about age 8, and most alleys offer party packages with food.</li>
  <li><strong>Escape rooms</strong> for ages 10 and up. Most rooms take 4 to 8 players, so book two rooms for a bigger group.</li>
</ul>

<h2>Food-Led Parties</h2>
<p>Pizza-making and cupcake-decorating parties have become popular because they solve two problems at once: the activity and the food are the same thing. Several Liverpool restaurants and cookery schools offer them. They suit smaller groups and children who like a bit of mess.</p>

<h2>Matching the Idea to the Age</h2>
<div class="article-table-scroll">
<table>
  <thead>
    <tr><th>Age</th><th>What usually works</th><th>What usually does not</th></tr>
  </thead>
  <tbody>
    <tr><td>4 to 6</td><td>Soft play, swimming, simple craft, entertainer at home</td><td>Anything needing concentration for more than 20 minutes</td></tr>
    <tr><td>7 to 9</td><td>Recording studio, football, climbing, bowling, pottery</td><td>Bouncy castles and soft play (too babyish, they will tell you)</td></tr>
    <tr><td>10 to 12</td><td>Recording studio, escape rooms, cinema plus food, museum trail</td><td>Big whole-class parties</td></tr>
    <tr><td>13 to 16</td><td>Recording studio, escape rooms, food-led, photoshoot, trampoline teen nights</td><td>Anything that feels organised by parents</td></tr>
  </tbody>
</table>
</div>

<h2>Questions to Ask Any Venue</h2>
<ul>
  <li>Is the space private for the party or shared with the public?</li>
  <li>How many adults need to stay, and where do they wait?</li>
  <li>Can we bring our own food and cake?</li>
  <li>What does each child take home?</li>
  <li>What happens if a child does not want to join in?</li>
</ul>
<p>That last question matters more than parents expect. At our studio the answer is that nobody is forced to sing solo. Shy children sing in the group takes, and the sound engineer mixes everyone together so the finished track sounds great whoever was loudest.</p>

<div class="article-callout">
  <h3>Working out the budget?</h3>
  <p>Our guide to <a href="/blog/how-much-does-kids-party-cost-liverpool.html">what a kids' party costs in Liverpool</a> shows how to compare per-child and package pricing properly.</p>
</div>
""",
    },
    {
        "slug": "birthday-party-ideas-8-to-12-year-olds",
        "tag": "Ages 8 to 12",
        "title": "Birthday Party Ideas for 8 to 12 Year Olds",
        "meta_title": "Birthday Party Ideas for 8 to 12 Year Olds | The Tween Party Guide",
        "description": "Too old for bouncy castles, too young for a night out. Party ideas that actually work for 8 to 12 year olds, plus the group size, structure and format tips that make the age group easy.",
        "image": "/assets/images/gallery-vocal-booth-group.jpg",
        "image_alt": "Group of 8 to 12 year olds in a recording booth at a CoverStar birthday party",
        "excerpt": "The 8 to 12 age group is the hardest to plan for and the easiest to get right once you understand what they want: to feel grown-up, to be with their real friends, and to make something.",
        "lead": "Somewhere around the eighth birthday, children stop wanting the parties they used to love. Bouncy castles are for babies. Pass the parcel is embarrassing. But they are not teenagers yet, and they still want a party. Parents call this the awkward age for birthdays. We host hundreds of parties for exactly this group every year, and it is not awkward at all once you know what they are after.",
        "body": """
<h2>What 8 to 12 Year Olds Actually Want</h2>
<ul>
  <li><strong>To feel older than they are.</strong> Anything that feels like a real grown-up activity, done properly, lands well. Anything with a cartoon on the banner does not.</li>
  <li><strong>Their real friends, not the whole class.</strong> By this age friendship groups have formed. Six to ten close friends is the natural size.</li>
  <li><strong>To do something, not just be somewhere.</strong> A room with food and music is not a party to a ten year old. An activity with a result is.</li>
  <li><strong>Something to show for it.</strong> A photo, a video, a recording, a thing they made. It is what they post, share and talk about.</li>
  <li><strong>A bit of independence</strong> while knowing a parent is nearby.</li>
</ul>

<h2>Ten Ideas That Work</h2>
<ol>
  <li><strong>Recording studio party.</strong> Pick a song, rehearse it, record it with a sound engineer and take home the track. Group chorus, optional solos for the birthday child, and a lyric screen so nobody needs to know the words. The age group loves the professional setting and the fact that the recording is real. Our packages run from <a href="/#packages">£199 for 8 children</a>.</li>
  <li><strong>Escape room.</strong> Brilliant from about 10 upwards. Book rooms that take 6 to 8 players and send an adult in with younger groups.</li>
  <li><strong>Cinema plus pizza.</strong> Simple and reliable. Let the birthday child pick the film and book seats together in advance.</li>
  <li><strong>Climbing or bouldering.</strong> Physical without being babyish, and the instructors handle the structure.</li>
  <li><strong>Pizza or cupcake making.</strong> Activity and food in one. Suits smaller groups.</li>
  <li><strong>Sleepover with a plan.</strong> Film, midnight feast, pancakes. Cap it at four or five guests and brief the parents on pickup times.</li>
  <li><strong>Bowling.</strong> Still a winner at 8 to 10. Lane bumpers off by request.</li>
  <li><strong>Football or multi-sport party</strong> with a coach on a 3G pitch.</li>
  <li><strong>Pottery painting.</strong> Calmer option for creative children.</li>
  <li><strong>Treasure hunt around the city or a park</strong> with teams, clues and a prize. Free, but needs adults per team.</li>
</ol>

<h2>Group Size: Smaller Is Better</h2>
<p>The biggest mistake parents make with this age group is inviting too many. A whole-class party for eleven year olds tends to split into cliques, leaves someone out, and costs a fortune. Eight to ten close friends is the sweet spot. It is also the group size most activity venues are built around. Our Gold and Platinum packages include 8 children and the Ultimate includes 10, with extra guests added per head if you need a few more.</p>

<h2>Mixed Groups</h2>
<p>Up to about age 9, mixed boy and girl groups are common and easy. From 10 to 12 some children want single-sex groups and some do not. Follow your child's lead rather than your own preference. Activity-led parties handle mixed groups far better than free-play parties because everyone has the same thing to do.</p>

<h2>Structure Without Looking Structured</h2>
<p>Children this age say they want to be left alone and then get bored within fifteen minutes if they are. The trick is a party with a built-in sequence that does not feel like adults organising games. A recording session is a good example: warm-up, rehearsal, group takes, solo takes, listen back, cake while the CDs print. Every stage is a natural next thing, and no adult has to blow a whistle.</p>

<h2>Phones, Photos and Consent</h2>
<p>Many 10 to 12 year olds have phones. Decide in advance whether they stay in bags during the activity, and tell parents on the invitation. For photos, ask every parent on the RSVP whether their child can appear in group pictures and whether those can be shared online. At our studio we never publish children's photos without parental consent, and the professionally edited photos on our Ultimate package are supplied privately to the booking parent.</p>

<h2>The Birthday Child Who Hates Attention</h2>
<p>Not every child wants to be the star. If yours would rather disappear into the group, choose an activity where the birthday child can lead or hang back as they like. In a recording session the solo takes are optional, and plenty of birthday children choose to sing only in the group. The track sounds just as good.</p>

<div class="article-callout">
  <h3>Choosing a song for the party?</h3>
  <p>The right song makes or breaks a recording party at this age. See our picks in <a href="/blog/best-songs-for-kids-popstar-party.html">Best Songs for a Kids' Pop-Star Party</a>.</p>
</div>
""",
    },
    {
        "slug": "teen-birthday-party-ideas-liverpool",
        "tag": "Teens",
        "title": "Teen Birthday Party Ideas in Liverpool",
        "meta_title": "Teen Birthday Party Ideas in Liverpool (Ages 13 to 16)",
        "description": "Birthday party ideas for teenagers in Liverpool that feel grown-up without a parent-organised vibe: recording studios, escape rooms, food-led nights, photoshoots and more.",
        "image": "/assets/images/solo-singer.jpg",
        "image_alt": "Teenager singing a solo take in a Liverpool recording studio booth",
        "excerpt": "Teenagers want a party that does not look like their parents planned it. Here is what works in Liverpool for 13 to 16 year olds, and how to stay involved without being in the room.",
        "lead": "Planning a party for a teenager is a diplomatic exercise. They want something to happen for their birthday. They do not want it to look like you made it happen. The solution is to find an experience that is genuinely cool on its own terms, book it, hand over the choices that matter to them, and then step back. Liverpool is a good city for this.",
        "body": """
<h2>Ground Rules for Teen Parties</h2>
<ul>
  <li><strong>Let them choose.</strong> The venue, the guest list, the music. Give a shortlist if you must, but the decision should be theirs.</li>
  <li><strong>Small groups.</strong> Six to ten is normal. Big parties are for the primary years.</li>
  <li><strong>Be present, not visible.</strong> Most venues require a supervising adult for under 16s. Find one with a separate space for parents.</li>
  <li><strong>Agree the social media rules before, not during.</strong> Who can be tagged, what gets posted. Teens are more protective of this than parents expect.</li>
</ul>

<h2>Ideas That Pass the Teen Test</h2>
<h3>Record a track in a real studio</h3>
<p>Our parties run up to age 16 and the teen sessions are some of the best we host. A group chooses a song, rehearses with a professional sound engineer in a working Liverpool studio, lays down group vocals and solos, and leaves with a mixed recording on vinyl-style CDs and as a download. Teens take the recording seriously, argue about harmonies, and genuinely care about the result. Parents relax in the studio lounge with the bar, out of sight. The Platinum and Ultimate packages include two songs, which suits groups who want to try a ballad and something upbeat. <a href="/#packages">Packages and prices</a>.</p>
<h3>Escape rooms</h3>
<p>Liverpool has plenty. Perfect for 13 to 16 because the teens run it themselves and adults wait outside. Book two rooms for groups over eight.</p>
<h3>Food-led nights</h3>
<p>Dinner at a restaurant of their choosing, a pizza-making session, or a dessert-bar crawl around the city centre. Food parties feel adult, which is exactly the point.</p>
<h3>Photoshoot party</h3>
<p>A studio photoshoot with friends, outfits and props is a popular teen party and leaves everyone with pictures they want to post. Our Ultimate package includes festival-style make-up and props and professionally edited photos alongside the recording, which combines two of the most popular teen formats into one afternoon.</p>
<h3>Trampoline park teen sessions</h3>
<p>Several parks around Liverpool run older-only evening sessions with music and lighting. Bouncing is fun at any age when there are no small children in the way.</p>
<h3>Cinema with a private twist</h3>
<p>Some Liverpool cinemas offer screen hire or premium seating for groups. A film of their choice plus food afterwards is low effort and high approval.</p>
<h3>Go-karting, climbing or bowling</h3>
<p>Classic active options that work well for 13 to 15 year olds in particular. Check minimum heights and ages for karting.</p>
<h3>A Liverpool music day</h3>
<p>For a music-obsessed teen, the Beatles Story or a Magical Mystery Tour bus, a wander round the Baltic Triangle, and a recording session to finish. Record a Liverpool classic and the day has a theme.</p>

<h2>The Supervision Question</h2>
<p>Most venues require at least one responsible adult to stay for under 16s. That is our rule too. What makes it workable is a venue with a separate adult space, so you are on hand without hovering. Ask about this before you book anywhere. A party where mum is sat at the edge of the room watching is a party no 15 year old wants.</p>

<h2>Budgeting for a Teen Party</h2>
<p>Teen parties are usually smaller than younger children's parties but cost more per head, because the activities are more involved and the food is proper food rather than crisps. A group of eight at an experience venue plus a meal is a typical format. Our <a href="/blog/how-much-does-kids-party-cost-liverpool.html">party cost guide</a> covers how to compare package and per-head pricing.</p>

<h2>What About the 16th?</h2>
<p>Sixteenth birthdays often get a bigger celebration. If a house party feels like too much, a studio session for a core group of friends in the afternoon followed by a meal or a larger gathering in the evening is a format that keeps everyone happy. The afternoon produces the recording and the photos; the evening is theirs.</p>

<div class="article-callout">
  <h3>Picking the song</h3>
  <p>Teens usually know exactly what they want to record. For groups that cannot agree, our guide to <a href="/blog/best-songs-for-kids-popstar-party.html">songs that work in a studio party</a> has a teen section.</p>
</div>
""",
    },
    {
        "slug": "best-songs-for-kids-popstar-party",
        "tag": "Songs",
        "title": "Best Songs for a Kids' Pop-Star Party",
        "meta_title": "Best Songs for a Kids' Pop-Star Party | Recording Studio Song Guide",
        "description": "Which songs work best when a group of children record in a studio? Our sound engineers share what makes a song easy to sing, plus picks by age and some Liverpool classics.",
        "image": "/assets/images/studio-cake-celebration.jpg",
        "image_alt": "Children celebrating with a birthday cake after recording their song at CoverStar",
        "excerpt": "Our engineers have recorded thousands of children's takes. Here is what makes a song work in the studio, and the tracks that come out sounding brilliant every time.",
        "lead": "The song is the single biggest decision at a recording studio party. Pick well and a group of nervous nine year olds sounds like a pop group by the second take. Pick badly and you spend the session chasing a chorus nobody can reach. We have recorded more children's parties than we can count, so here is what our sound engineers have learned, and the songs they recommend.",
        "body": """
<h2>What Makes a Song Work in the Studio</h2>
<ul>
  <li><strong>A big, repeated chorus.</strong> The chorus is where the whole group sings together, and repetition means everyone has it by the end of rehearsal. Verses can be shared out or sung by the birthday child.</li>
  <li><strong>A comfortable vocal range.</strong> Children's voices sit higher than adults' but do not have the power for big belting notes. Songs built around huge sustained high notes are hard work for anyone under 14.</li>
  <li><strong>Mid to upbeat tempo.</strong> Energy carries a group. Slow ballads expose every wobble and can feel long.</li>
  <li><strong>Three to four minutes.</strong> Long enough to feel like a real song, short enough to rehearse and record properly within the session.</li>
  <li><strong>Clean lyrics.</strong> Many chart hits have a clean radio edit. Check the words before you commit, especially for the 8 to 12 group.</li>
  <li><strong>A song everyone actually knows.</strong> The lyric screen helps, but a group that already sings along to it in the car will sound far more confident.</li>
</ul>

<h2>Songs That Come Out Brilliantly for Ages 7 to 10</h2>
<ul>
  <li>"Shake It Off" by Taylor Swift. Practically designed for a group chorus.</li>
  <li>"Happy" by Pharrell Williams. Easy range, infectious, impossible to sing badly.</li>
  <li>"Can't Stop the Feeling!" by Justin Timberlake. Big singalong chorus.</li>
  <li>"Roar" by Katy Perry. A confidence anthem, which is often exactly the mood.</li>
  <li>"Best Day of My Life" by American Authors. Perfect birthday sentiment and an easy "oh-oh-oh" hook.</li>
  <li>"Count on Me" by Bruno Mars. Gentler option for a group of close friends.</li>
  <li>"Let It Go" from Frozen or "How Far I'll Go" from Moana for younger film fans. The big notes at the end need a confident birthday child.</li>
  <li>"We Don't Talk About Bruno" from Encanto. Great for a group because the parts can be shared out.</li>
</ul>

<h2>Songs for Ages 10 to 13</h2>
<ul>
  <li>"Flowers" by Miley Cyrus. Strong, singable, and the age group knows every word.</li>
  <li>"As It Was" by Harry Styles. Mid-tempo and easy on the voice.</li>
  <li>"Dance Monkey" by Tones and I. Distinctive and fun, though the chorus sits quite high.</li>
  <li>"Shotgun" by George Ezra. Relaxed range, happy singalong.</li>
  <li>"Levitating" by Dua Lipa. Upbeat, with a chorus that carries a group.</li>
  <li>"Don't Stop Me Now" by Queen. A perennial, and parents love it too.</li>
  <li>"Dancing Queen" or "Mamma Mia" by ABBA. Cross-generational and built for groups.</li>
</ul>

<h2>Songs for Teens</h2>
<p>Teens usually arrive with the song chosen. When they ask for advice, these are the ones that record well:</p>
<ul>
  <li>"Espresso" by Sabrina Carpenter. Current, upbeat, group-friendly.</li>
  <li>"Birds of a Feather" by Billie Eilish. A gentler option that suits a close friendship group.</li>
  <li>"Cruel Summer" or "Anti-Hero" by Taylor Swift. Reliable for any Swiftie group.</li>
  <li>"Shivers" or "Perfect" by Ed Sheeran, depending on whether they want up or down tempo.</li>
  <li>"What Makes You Beautiful" by One Direction. Still a guaranteed group singalong.</li>
  <li>"Someone You Loved" by Lewis Capaldi for a confident soloist with a group backing on the chorus.</li>
</ul>
<p>Check the clean version is available for anything current. We will always tell you if a lyric needs to come out.</p>

<h2>Liverpool Classics</h2>
<p>You are recording in the city that gave the world The Beatles, and plenty of families lean into it. These work especially well with children:</p>
<ul>
  <li>"Yellow Submarine". The easiest Beatles song for a group, and great fun.</li>
  <li>"Hey Jude". The "na na na" outro is made for a studio full of children.</li>
  <li>"Here Comes the Sun". Gentle, happy and within everyone's range.</li>
  <li>"All You Need Is Love". A simple, joyful chorus.</li>
  <li>"Twist and Shout". High energy and a brilliant way to end a session.</li>
</ul>

<h2>Songs to Approach With Care</h2>
<ul>
  <li><strong>Power ballads</strong> such as Whitney Houston or Adele. Beautiful, but the range defeats most groups under 14. Fine for a strong solo birthday child with the group on backing.</li>
  <li><strong>Fast rap sections.</strong> Fun to attempt, hard to record cleanly in one session.</li>
  <li><strong>Anything only one child knows.</strong> The group needs to carry it.</li>
  <li><strong>Very long songs.</strong> Over five minutes eats into rehearsal time.</li>
</ul>

<h2>How We Help on the Day</h2>
<p>You do not need to get this perfect on your own. When you book we ask for your song choice in advance so we can have the backing track and lyrics ready. Our sound engineer runs a warm-up and a rehearsal, splits up the parts, and records the group takes first so everyone relaxes before any solos. After recording, the engineer edits and mixes the track so the finished version sounds polished whoever hit the notes. On the Platinum and Ultimate packages you record two songs, which is a good way to pair a fast song with a slower one. Browse our <a href="/#packages">packages</a>, or read about <a href="/">what happens at a CoverStar party</a>.</p>

<div class="article-callout">
  <h3>Can't decide between two songs?</h3>
  <p>Call us on <a href="tel:08006897827">0800 689 7827</a> and tell us the age and size of the group. We will tell you honestly which one will sound better.</p>
</div>
""",
    },
]

# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def esc(s):
    return html.escape(s, quote=True)


def word_count(fragment):
    text = re.sub(r"<[^>]+>", " ", fragment)
    return len(text.split())


def read_minutes(post):
    words = word_count(post["body"]) + word_count(post["lead"])
    return max(1, round(words / 200))


def nice_date(iso):
    d = date.fromisoformat(iso)
    return d.strftime("%-d %B %Y")


def post_url(post):
    return f"{SITE}/blog/{post['slug']}.html"


def article_schema(post):
    return (
        '  <script type="application/ld+json">\n'
        "  {\n"
        '    "@context": "https://schema.org",\n'
        '    "@graph": [\n'
        "      {\n"
        '        "@type": "Article",\n'
        f'        "headline": "{esc(post["title"])}",\n'
        f'        "description": "{esc(post["description"])}",\n'
        f'        "image": "{SITE}{post["image"]}",\n'
        f'        "datePublished": "{PUBLISHED}",\n'
        f'        "dateModified": "{PUBLISHED}",\n'
        f'        "author": {{"@type": "Organization", "name": "{AUTHOR}", "url": "{SITE}/"}},\n'
        '        "publisher": {"@type": "Organization", "name": "CoverStar Kids Parties", '
        f'"logo": {{"@type": "ImageObject", "url": "{SITE}/assets/images/coverstar-logo.jpg"}}}},\n'
        f'        "mainEntityOfPage": "{post_url(post)}"\n'
        "      },\n"
        "      {\n"
        '        "@type": "BreadcrumbList",\n'
        '        "itemListElement": [\n'
        f'          {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{SITE}/"}},\n'
        f'          {{"@type": "ListItem", "position": 2, "name": "Blog", "item": "{SITE}/blog/"}},\n'
        f'          {{"@type": "ListItem", "position": 3, "name": "{esc(post["title"])}", "item": "{post_url(post)}"}}\n'
        "        ]\n"
        "      }\n"
        "    ]\n"
        "  }\n"
        "  </script>\n"
    )


def index_schema():
    items = ",\n".join(
        f'          {{"@type": "ListItem", "position": {i + 1}, "url": "{post_url(p)}", "name": "{esc(p["title"])}"}}'
        for i, p in enumerate(POSTS)
    )
    return (
        '  <script type="application/ld+json">\n'
        "  {\n"
        '    "@context": "https://schema.org",\n'
        '    "@type": "CollectionPage",\n'
        '    "name": "Party Planning Advice",\n'
        f'    "url": "{SITE}/blog/",\n'
        '    "description": "Practical advice for parents planning children\'s birthday parties in Liverpool, from the team at CoverStar Kids Parties.",\n'
        '    "isPartOf": {"@type": "WebSite", "name": "CoverStar Kids Parties", "url": "' + SITE + '/"},\n'
        '    "mainEntity": {\n'
        '      "@type": "ItemList",\n'
        '      "itemListElement": [\n'
        f"{items}\n"
        "      ]\n"
        "    }\n"
        "  }\n"
        "  </script>\n"
    )


def card(post):
    return f"""
        <article class="blog-card">
          <a href="/blog/{post['slug']}.html"><img src="{post['image']}" alt="{esc(post['image_alt'])}" class="blog-card-img" loading="lazy"></a>
          <div class="blog-card-body">
            <span class="blog-tag">{esc(post['tag'])}</span>
            <h3><a href="/blog/{post['slug']}.html">{esc(post['title'])}</a></h3>
            <p>{esc(post['excerpt'])}</p>
            <a href="/blog/{post['slug']}.html" class="blog-read-more">Read the guide →</a>
            <div class="blog-meta">{nice_date(PUBLISHED)} · {read_minutes(post)} min read</div>
          </div>
        </article>"""


def render_post(post):
    others = [p for p in POSTS if p["slug"] != post["slug"]][:3]
    extra_meta = (
        f'  <meta property="og:type" content="article">\n'
        f'  <meta property="og:title" content="{esc(post["title"])}">\n'
        f'  <meta property="og:description" content="{esc(post["description"])}">\n'
        f'  <meta property="og:url" content="{post_url(post)}">\n'
        f'  <meta property="og:image" content="{SITE}{post["image"]}">\n'
        f'  <meta property="article:published_time" content="{PUBLISHED}">\n'
    )
    head = HEAD.format(
        title=esc(post["meta_title"]),
        description=esc(post["description"]),
        canonical=post_url(post),
        extra_meta=extra_meta,
        schema=article_schema(post),
    )
    body = f"""
  <!-- Editorial status: published for review by the CoverStar team. Verify prices, venue details and third-party facts before promoting. -->

  <!-- Page Banner -->
  <section class="section-dark" style="padding: 48px 0; text-align: center;">
    <div class="container">
      <div class="article-breadcrumb"><a href="/">Home</a> › <a href="/blog/">Blog</a> › {esc(post['tag'])}</div>
      <h1>{esc(post['title'])}</h1>
      <p style="max-width: 750px; margin: 0 auto; color: var(--color-text-light);">By {AUTHOR} · {nice_date(PUBLISHED)} · {read_minutes(post)} min read</p>
    </div>
  </section>

  <!-- Article -->
  <section class="section">
    <div class="container">
      <div class="article-wrap">
        <img src="{post['image']}" alt="{esc(post['image_alt'])}" class="article-hero-img">
        <p class="article-lead">{post['lead']}</p>
        <div class="article-body">
{post['body'].strip()}
        </div>
{CTA_BLOCK}
      </div>
    </div>
  </section>

  <!-- Related posts -->
  <section class="section section-alt related-posts">
    <div class="container">
      <h2>More Party Planning Advice</h2>
      <p style="text-align: center; color: var(--color-text-muted);">Practical guides from the CoverStar Kids Parties team.</p>
      <div class="blog-grid">{''.join(card(p) for p in others)}
      </div>
      <p style="text-align: center; margin-top: 32px;"><a href="/blog/" class="btn btn-outline-gold">All Articles</a></p>
    </div>
  </section>
"""
    return head + TOP_BAR_AND_HEADER + body + FOOTER


def render_index():
    head = HEAD.format(
        title="Kids' Party Planning Advice for Liverpool Parents | CoverStar Blog",
        description="Practical guides for planning a children's birthday party in Liverpool: costs, venues, ideas by age, and the best songs for a pop-star recording party.",
        canonical=f"{SITE}/blog/",
        extra_meta="",
        schema=index_schema(),
    )
    body = f"""
  <!-- Page Banner -->
  <section class="section-dark" style="padding: 48px 0; text-align: center;">
    <div class="container">
      <div style="font-size: 14px; text-transform: uppercase; color: var(--color-primary); margin-bottom: 8px;">The CoverStar Blog</div>
      <h1>Party Planning Advice</h1>
      <p style="max-width: 750px; margin: 0 auto; color: var(--color-text-light);">Honest, practical guides for Liverpool parents, written by the team that hosts hundreds of children's parties every year.</p>
    </div>
  </section>

  <!-- Posts -->
  <section class="section">
    <div class="container">
      <div class="blog-grid">{''.join(card(p) for p in POSTS)}
      </div>
    </div>
  </section>

  <!-- Intro / trust -->
  <section class="section section-alt">
    <div class="container">
      <div class="article-wrap article-body">
        <h2 style="margin-top: 0; text-align: center;">Why We Write These Guides</h2>
        <p>CoverStar Experiences has hosted children's recording studio parties in Liverpool since 2013. Over that time we have answered the same questions from thousands of parents: how much should a party cost, what works for a ten year old, how do we get a group of children to sing, and where on earth do you park in the city centre. These articles are our answers, written down. Where we recommend our own parties we say so plainly, and where another kind of party would suit your child better we say that too.</p>
        <p style="text-align: center; margin-top: 28px;"><a href="/about-coverstar/" class="btn btn-outline-gold">About CoverStar</a> <a href="/contact/#enquire" class="btn btn-pink" style="margin-left: 10px;">Check a Party Date</a></p>
      </div>
    </div>
  </section>
"""
    return head + TOP_BAR_AND_HEADER + body + FOOTER


def main():
    os.makedirs(BLOG_DIR, exist_ok=True)
    with open(os.path.join(BLOG_DIR, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(render_index())
    for post in POSTS:
        with open(os.path.join(BLOG_DIR, f"{post['slug']}.html"), "w", encoding="utf-8") as fh:
            fh.write(render_post(post))
    print(f"Wrote blog/index.html and {len(POSTS)} posts to {BLOG_DIR}")
    for post in POSTS:
        print(f"  {post['slug']}.html  ({word_count(post['body']) + word_count(post['lead'])} words)")


if __name__ == "__main__":
    main()
