import hot1 from '../assets/Hot_Cold/Hot1.jpg'
import hot2 from '../assets/Hot_Cold/Hot2.jpg'
import hot3 from '../assets/Hot_Cold/Hot3.jpg'
import cold1 from '../assets/Hot_Cold/Cold1.jpg'
import cold2 from '../assets/Hot_Cold/Cold2.jpg'
import cold3 from '../assets/Hot_Cold/Cold83.jpg'
import almondCroissant from '../assets/Pastries_Specials/Almond Croissant.jpg'
import bananaBread from '../assets/Pastries_Specials/Brown Butter Banana Bread.jpg'
import matchaScone from '../assets/Pastries_Specials/Matcha Scone.jpg'
import special1 from '../assets/Pastries_Specials/special1.jpg'
import special2 from '../assets/Pastries_Specials/special2.jpg'
import special3 from '../assets/Pastries_Specials/special3.jpg'

export const menuItems = [
  // HOT
  {
    id: 1,
    category: "hot",
    name: "Driftwood Espresso",
    description: "Double shot, dark roast, with notes of cedar and dark chocolate.",
    price: "KES 350",
    image: hot1,
  },
  {
    id: 2,
    category: "hot",
    name: "Flat White",
    description: "Velvety microfoam over a ristretto shot. Clean and bold.",
    price: "KES 420",
    image: hot2,
  },
  {
    id: 3,
    category: "hot",
    name: "Spiced Chai Latte",
    description: "House-blended chai with cinnamon, cardamom, and steamed oat milk.",
    price: "KES 480",
    image: hot3,
  },

  // COLD
  {
    id: 4,
    category: "cold",
    name: "Cold Brew",
    description: "Steeped 18 hours. Smooth, low-acid, served over clear ice.",
    price: "KES 450",
    image: cold1,
  },
  {
    id: 5,
    category: "cold",
    name: "Iced Lavender Latte",
    description: "House lavender syrup, espresso, whole milk over ice.",
    price: "KES 520",
    image: cold2,
  },
  {
    id: 6,
    category: "cold",
    name: "Mango Cold Foam",
    description: "Cold brew topped with salted mango cold foam. Summer in a cup.",
    price: "KES 580",
    image: cold3,
  },

  // PASTRIES
  {
    id: 7,
    category: "pastries",
    name: "Almond Croissant",
    description: "Twice-baked with frangipane, toasted almonds, and powdered sugar.",
    price: "KES 380",
    image: almondCroissant,
  },
  {
    id: 8,
    category: "pastries",
    name: "Brown Butter Banana Bread",
    description: "Moist, dense, with walnuts and a brown butter glaze.",
    price: "KES 350",
    image: bananaBread,
  },
  {
    id: 9,
    category: "pastries",
    name: "Matcha Scone",
    description: "Ceremonial grade matcha with white chocolate chips and lemon zest.",
    price: "KES 400",
    image: matchaScone,
  },

  // SPECIALS
  {
    id: 10,
    category: "specials",
    name: "Driftwood Signature",
    description: "Espresso, coconut milk, cardamom, and a hint of rose. Our flagship.",
    price: "KES 600",
    image: special1,
  },
  {
    id: 11,
    category: "specials",
    name: "Fog Cutter",
    description: "Cold brew, oat milk, sea salt caramel, and house cinnamon syrup.",
    price: "KES 620",
    image: special2,
  },
  {
    id: 12,
    category: "specials",
    name: "Ember & Oak",
    description: "Smoked vanilla syrup, espresso, steamed whole milk, caramel drizzle.",
    price: "KES 650",
    image: special3,
  },
];

import gallery2 from '../assets/gallary/2.jpg'
import gallery3 from '../assets/gallary/3.jpg'
import gallery5 from '../assets/gallary/5.jpg'
import gallery6 from '../assets/gallary/6.jpg'
import gallery7 from '../assets/gallary/7.jpg'
import gallery8 from '../assets/gallary/8.jpg'

export const galleryImages = [
  { id: 2, src: gallery2, alt: 'Café interior', size: 'wide' },
  { id: 3, src: gallery3, alt: 'Coffee roaster', size: 'normal' },
  { id: 5, src: gallery5, alt: 'Pastry display', size: 'normal' },
  { id: 6, src: gallery6, alt: 'Espresso pour', size: 'wide' },
  { id: 7, src: gallery7, alt: 'Latte art', size: 'normal' },
  { id: 8, src: gallery8, alt: 'Coffee cupping', size: 'normal' },
];

export const reviews = [
  {
    id: 1,
    name: 'Sarah Johnson',
    date: 'February 10, 2026',
    rating: 5,
    review: 'The atmosphere is so inviting, and their cappuccino is absolutely perfect! I love working remotely from here — the vibe keeps me productive and calm.',
    avatar: 'SJ',
  },
  {
    id: 2,
    name: 'Michael Chen',
    date: 'January 15, 2026',
    rating: 5,
    review: 'Their cold brew is the best I\'ve had in the city — smooth with no bitterness. The pastries are baked fresh daily and pair perfectly with any drink.',
    avatar: 'MC',
  },
  {
    id: 3,
    name: 'Amara Osei',
    date: 'February 20, 2026',
    rating: 5,
    review: 'Driftwood Café is my go-to spot. The staff remembers my order and the seasonal specials are always worth trying. Truly a hidden gem.',
    avatar: 'AO',
  },
  {
    id: 4,
    name: 'Lena Fischer',
    date: 'February 22, 2026',
    rating: 4,
    review: 'Lovely space with incredible attention to detail. The lavender honey latte is unlike anything I\'ve tasted. Will definitely be coming back.',
    avatar: 'LF',
  },
  {
    id: 5,
    name: 'James Mwangi',
    date: 'March 28, 2025',
    rating: 5,
    review: 'As someone who takes coffee seriously, I\'m impressed. The single origin pour-over was flawlessly executed. Knowledgeable baristas too.',
    avatar: 'JM',
  },
  {
    id: 6,
    name: 'Priya Sharma',
    date: 'March 28, 2025',
    rating: 5,
    review: 'Perfect spot for a date or a quiet afternoon. The cardamom rose cold brew is poetry in a glass. Already recommended it to everyone I know.',
    avatar: 'PS',
  },
]

// ── Merch ────────────────────────────────────────────────────────────────────
import merch1 from '../assets/Merch/M1.jpeg'
import merch2 from '../assets/Merch/M2.jpeg'
import merch3 from '../assets/Merch/M3.jpeg'
import merch4 from '../assets/Merch/M4.jpeg'
import merch5 from '../assets/Merch/M5.jpeg'
import merch6 from '../assets/Merch/M6.jpeg'

export const merchItems = [
  {
    id: 18,
    name: 'Driftwood Bucket Hat',
    category: 'merch',
    subcategory: 'Accessories',
    description: 'A wide-brim black bucket hat with "Driftwood cafe\'" embroidered in warm cream lettering. Features an adjustable chin strap cord for a secure, stylish fit — perfect for sunny mornings and café runs.',
    price: 'KES 2,200',
    tag: 'Bestseller',
    image: merch1,
  },
  {
    id: 19,
    name: 'Signature Canvas Tote',
    category: 'merch',
    subcategory: 'Accessories',
    description: 'A sturdy all-black canvas tote bearing the full Driftwood Café identity — EST. 2024, bold wordmark, and the tagline "Coffee · Community · Craft. Brewed with purpose." Spacious, reusable, and unmistakably Driftwood.',
    price: 'KES 1,800',
    tag: 'New',
    image: merch2,
  },
  {
    id: 20,
    name: 'Matte Black Ceramic Mug',
    category: 'merch',
    subcategory: 'Drinkware',
    description: 'A smooth matte-black ceramic mug with "Driftwood cafe\'" printed in elegant cream-gold serif lettering. The perfect vessel for your morning ritual — understated, weighty, and built to be savoured.',
    price: 'KES 1,600',
    tag: null,
    image: merch3,
  },
  {
    id: 21,
    name: 'Driftwood Travel Tumbler',
    category: 'merch',
    subcategory: 'Drinkware',
    description: 'An insulated matte-black travel tumbler with a ribbed silicone grip band, stainless steel rim, and secure flip-top lid. Keeps your brew hot on the go, branded with "Driftwood cafe\'" for the commuter who doesn\'t compromise.',
    price: 'KES 3,500',
    tag: 'Bestseller',
    image: merch4,
  },
  {
    id: 22,
    name: 'Coffee Into Code Tee — Navy',
    category: 'merch',
    subcategory: 'Apparel',
    description: 'A navy blue crew-neck tee featuring a playful illustrated graphic: "I Turn Coffee into Code" surrounded by steaming cups and coffee beans. Soft, comfortable, and made for the developer who runs on espresso.',
    price: 'KES 2,800',
    tag: null,
    image: merch5,
  },
  {
    id: 23,
    name: 'Coffee Into Code Tee — Grey',
    category: 'merch',
    subcategory: 'Apparel',
    description: 'A heather grey crew-neck tee with a bold, high-contrast "I Turn Coffee into Code" graphic print. Minimal, punchy, and unmistakably built for the caffeine-fuelled creative. A Driftwood cult classic.',
    price: 'KES 2,800',
    tag: 'New',
    image: merch6,
  },
]
