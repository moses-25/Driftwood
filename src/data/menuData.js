export const menuItems = [
  // HOT
  {
    id: 1,
    category: "hot",
    name: "Driftwood Espresso",
    description: "Double shot, dark roast, with notes of cedar and dark chocolate.",
    price: "$3.50",
    image: "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?w=400&q=80",
  },
  {
    id: 2,
    category: "hot",
    name: "Flat White",
    description: "Velvety microfoam over a ristretto shot. Clean and bold.",
    price: "$4.25",
    image: "https://images.unsplash.com/photo-1534778101976-62847782c213?w=400&q=80",
  },
  {
    id: 3,
    category: "hot",
    name: "Spiced Chai Latte",
    description: "House-blended chai with cinnamon, cardamom, and steamed oat milk.",
    price: "$4.75",
    image: "https://images.unsplash.com/photo-1571934811356-5cc061b6821f?w=400&q=80",
  },

  // COLD
  {
    id: 4,
    category: "cold",
    name: "Cold Brew",
    description: "Steeped 18 hours. Smooth, low-acid, served over clear ice.",
    price: "$4.50",
    image: "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=400&q=80",
  },
  {
    id: 5,
    category: "cold",
    name: "Iced Lavender Latte",
    description: "House lavender syrup, espresso, whole milk over ice.",
    price: "$5.25",
    image: "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?w=400&q=80",
  },
  {
    id: 6,
    category: "cold",
    name: "Mango Cold Foam",
    description: "Cold brew topped with salted mango cold foam. Summer in a cup.",
    price: "$5.75",
    image: "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400&q=80",
  },

  // PASTRIES
  {
    id: 7,
    category: "pastries",
    name: "Almond Croissant",
    description: "Twice-baked with frangipane, toasted almonds, and powdered sugar.",
    price: "$3.75",
    image: "https://images.unsplash.com/photo-1509365465985-25d11c17e812?w=400&q=80",
  },
  {
    id: 8,
    category: "pastries",
    name: "Brown Butter Banana Bread",
    description: "Moist, dense, with walnuts and a brown butter glaze.",
    price: "$3.50",
    image: "https://images.unsplash.com/photo-1605286978633-2dec93ff88a2?w=400&q=80",
  },
  {
    id: 9,
    category: "pastries",
    name: "Matcha Scone",
    description: "Ceremonial grade matcha with white chocolate chips and lemon zest.",
    price: "$4.00",
    image: "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=400&q=80",
  },

  // SPECIALS
  {
    id: 10,
    category: "specials",
    name: "Driftwood Signature",
    description: "Espresso, coconut milk, cardamom, and a hint of rose. Our flagship.",
    price: "$6.00",
    image: "https://images.unsplash.com/photo-1511920170033-f8396924c348?w=400&q=80",
  },
  {
    id: 11,
    category: "specials",
    name: "Fog Cutter",
    description: "Cold brew, oat milk, sea salt caramel, and house cinnamon syrup.",
    price: "$6.25",
    image: "https://images.unsplash.com/photo-1572442388796-11668a67e53d?w=400&q=80",
  },
  {
    id: 12,
    category: "specials",
    name: "Ember & Oak",
    description: "Smoked vanilla syrup, espresso, steamed whole milk, caramel drizzle.",
    price: "$6.50",
    image: "https://images.unsplash.com/photo-1485808191679-5f86510cbae9?w=400&q=80",
  },
];

export const galleryImages = [
  { id: 1, src: '/src/assets/gallary/1.jpg', alt: 'Barista at work', size: 'tall' },
  { id: 2, src: '/src/assets/gallary/2.jpg', alt: 'Café interior', size: 'wide' },
  { id: 3, src: '/src/assets/gallary/3.jpg', alt: 'Coffee roaster', size: 'normal' },
  { id: 4, src: '/src/assets/gallary/4.jpg', alt: 'Coffee tools', size: 'normal' },
  { id: 5, src: '/src/assets/gallary/5.jpg', alt: 'Pastry display', size: 'normal' },
  { id: 6, src: '/src/assets/gallary/6.jpg', alt: 'Espresso pour', size: 'wide' },
  { id: 7, src: '/src/assets/gallary/7.jpg', alt: 'Latte art', size: 'normal' },
  { id: 8, src: '/src/assets/gallary/8.jpg', alt: 'Coffee cupping', size: 'normal' },
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