/**
 * CoverStar Kids Parties - Central Data Store
 * Domain: coverstarkidsparties.co.uk
 * Single source of truth for business details, packages, FAQs, and reviews.
 */

const COVERSTAR_DATA = {
  business: {
    brandName: "CoverStar Kids Parties",
    legalEntity: "CoverStar Experiences",
    parentBrand: "CoverStar Experiences",
    parentUrl: "https://www.coverstarexperiences.co.uk/",
    domain: "coverstarkidsparties.co.uk",
    phoneDisplay: "0800 689 7827",
    phoneTel: "08006897827",
    email: "info@coverstarexperiences.co.uk",
    venueName: "Prohibition Recording Studios",
    addressLine1: "24 Arrad Street",
    addressLine2: "Georgian Quarter, Liverpool City Centre",
    city: "Liverpool",
    county: "Merseyside",
    postcode: "L1 3BP",
    establishedYear: 2013,
    tripAdvisorAwards: [2014, 2015, 2016, 2018, 2019, 2021, 2022, 2023, 2024, 2025],
    tripAdvisorCount: "422+",
    googleRating: "5.0",
    ageRange: "7 to 16",
    supervisionRule: "At least one parent or guardian must remain at the studio throughout the celebration."
  },

  images: {
    logo: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2016/08/CoverStar-Experiences-Master-Logo-Centered-150x150.jpg",
    favicon: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2016/08/cropped-CoverStar-Experiences-Master-Logo-Centered-100x100.jpg",
    heroMain: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2024/05/Kids-parties-liverpool-Coverstar.jpg",
    singingSolo: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2018/07/Birthday-girl-singing-solo.jpg",
    goldCds: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2018/07/23.07.2018-1-4356.jpg",
    soloTime: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2018/07/Solo-time.jpg",
    gabyParty: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2018/11/Gabys-Party-23-7295.jpg",
    photographerAddon: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2018/07/CoverStar-photographer-add-on-2.jpg",
    smilingGroup: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2018/07/Kids-party-smiling-before-they-sing.jpg",
    makeupHost: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2018/07/Party-host-with-birthday-girl-doing-makeup.jpg",
    invites: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2019/07/CoverStar-Invites-1-600x400.jpg",
    cakeLounge: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2020/06/CoverStar-20.10.2019-1pm-Laurens-Birthday-28-600x400.jpg",
    boothGroup: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2019/07/CoverStar-20.04.2019-10.30am-Mayas-Party-18-600x400.jpg",
    vinylStack: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2018/07/CoverStar-signature-gold-personlsied-Cds-600x400.jpg",
    tripadvisorBadge: "https://www.coverstarexperiences.co.uk/wp-content/uploads/2025/11/CoverStar-Experiences-Travellers-Choice-2025.png"
  },

  packages: [
    {
      id: "gold",
      name: "Gold Popstar Party",
      price: 199.00,
      guestsIncluded: 8,
      extraGuestPrice: 25.00,
      duration: "1.5 hours",
      songs: 1,
      highlight: false,
      features: [
        "1 Song Recording",
        "Backing Tracks & Lyric Screen Included",
        "Professional Sound Engineer",
        "1.5 Hours Studio Time",
        "One Black Vinyl Style CD for VIP",
        "Digital Download Copy"
      ]
    },
    {
      id: "platinum",
      name: "Platinum Popstar Party",
      price: 280.00,
      guestsIncluded: 8,
      extraGuestPrice: 35.00,
      duration: "2.0 hours",
      songs: 2,
      highlight: true,
      badgeText: "Most Popular",
      features: [
        "2 Song Recordings",
        "Backing Tracks & Lyric Screen Included",
        "Professional Sound Engineer",
        "2.0 Hours Studio Time",
        "Black Vinyl Style CDs for Everyone",
        "One Gold Personalised Vinyl Style CD for VIP",
        "Digital Download Copy"
      ]
    },
    {
      id: "ultimate",
      name: "Ultimate Popstar Party",
      price: 380.00,
      guestsIncluded: 10,
      extraGuestPrice: 38.00,
      duration: "2.0 hours",
      songs: 2,
      highlight: false,
      features: [
        "2 Song Recordings",
        "2.0 Hours Studio Time",
        "Dedicated Party Host Included",
        "Professionally Edited Photos",
        "Festival Style Make-up & Props",
        "Black Vinyl Style CDs for Everyone",
        "One Gold Personalised Vinyl Style CD for VIP",
        "Digital Download Copy"
      ]
    }
  ],

  faqs: [
    {
      question: "Do the children need to be confident or good singers?",
      answer: "Not at all! Our recording studio parties are all about having fun and celebrating together. Children record in group takes as well as optional solo takes. Our professional sound engineer guides them through rehearsals and uses digital mixing techniques to make everyone sound great."
    },
    {
      question: "What age range are the parties suitable for?",
      answer: "Our popstar recording experiences are ideal for children aged 7 through to 16. We tailor the studio hosting, song rehearsals, and party games to match the age group of your child and their friends."
    },
    {
      question: "Do parents need to remain at the studio during the party?",
      answer: "Health and safety is our top priority. We require at least one parent or responsible guardian to remain at Prohibition Recording Studios for the duration of the party. Parents are welcome to relax on our studio lounge sofas and watch the recording session!"
    },
    {
      question: "Can we bring our own food, drinks, and birthday cake?",
      answer: "Yes! Kitchen and lounge facilities are available. Parents often bring a birthday cake, snacks, or order hot food (such as Domino's pizza) to enjoy during the lounge break while the CDs are being printed."
    },
    {
      question: "Where is the venue located and is there parking nearby?",
      answer: "Our venue is located inside Prohibition Recording Studios at 24 Arrad Street in Liverpool City Centre (Georgian Quarter, L1 3BP). On-street parking and nearby pay-and-display car parks are available within short walking distance."
    },
    {
      question: "How do we check date availability and book?",
      answer: "Fill out our online availability form or call our friendly team on 0800 689 7827. Once your date and time slot are provisionally confirmed, a £50 deposit secures your party slot."
    }
  ],

  reviews: [
    {
      author: "Vicky H",
      source: "TripAdvisor",
      stars: 5,
      text: "Booked here for my daughter's 10th birthday and I can honestly say it has been her best experience ever! From the original enquiry with Ruby to receiving our pictures and song from Matt, they have both been fantastic. It was a magical experience for a group of 9/10 year old girls hearing their song played back."
    },
    {
      author: "Clare B",
      source: "TripAdvisor",
      stars: 5,
      text: "From the moment we booked there was constant communication. They offered suggestions regarding catering and took lovely photos on the day that dropped into my inbox. We really couldn't recommend this experience highly enough!"
    },
    {
      author: "Jen",
      source: "TripAdvisor",
      stars: 5,
      text: "On the day the party experience and venue exceeded our expectations. Matt and Holly were fantastic and really went the extra mile to make our daughter's day special. The girls all loved being presented with their own CDs!"
    }
  ]
};
