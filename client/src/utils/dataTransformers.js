/**
 * Get placeholder image based on category
 */
const getPlaceholderImage = (categoryName) => {
  // Return a data URL for a simple placeholder SVG
  const color = {
    'Hot Coffee': '#8B4513',
    'Cold Coffee': '#4682B4',
    'Pastries': '#DEB887',
    'Specials': '#DAA520',
    'Merchandise': '#696969',
  }[categoryName] || '#8B4513';

  return `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E%3Crect fill='${encodeURIComponent(color)}' width='200' height='200' opacity='0.2'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial' font-size='16' fill='${encodeURIComponent(color)}' opacity='0.6'%3ENo Image%3C/text%3E%3C/svg%3E`;
};

/**
 * Transform backend product data to frontend menu item format
 */
export const transformProductToMenuItem = (product) => {
  // Map backend category names to frontend category keys
  const categoryMap = {
    'Hot Coffee': 'hot',
    'Cold Coffee': 'cold',
    'Pastries': 'pastries',
    'Specials': 'specials',
    'Merchandise': 'merch',
  };

  return {
    id: product.id,
    category: categoryMap[product.category_name] || 'hot',
    name: product.name,
    description: product.description,
    price: `KES ${product.price.toFixed(0)}`,
    image: product.image_url || getPlaceholderImage(product.category_name),
    tag: product.tag || null,
    // Additional fields that might be useful
    isAvailable: product.is_available,
    stockQuantity: product.stock_quantity,
    calories: product.calories,
    preparationTime: product.preparation_time,
    averageRating: product.average_rating,
    reviewCount: product.review_count,
  };
};

/**
 * Transform multiple products
 */
export const transformProducts = (products) => {
  return products.map(transformProductToMenuItem);
};

/**
 * Transform backend category data to frontend format
 */
export const transformCategory = (category) => {
  const categoryKeyMap = {
    'Hot Coffee': 'hot',
    'Cold Coffee': 'cold',
    'Pastries': 'pastries',
    'Specials': 'specials',
    'Merchandise': 'merch',
  };

  return {
    id: category.id,
    key: categoryKeyMap[category.name] || category.name.toLowerCase(),
    label: category.name,
    description: category.description,
    isActive: category.is_active,
    productCount: category.product_count,
    imageUrl: category.image_url,
  };
};

/**
 * Transform cart items to backend order format
 */
export const transformCartToOrderItems = (cartItems) => {
  return cartItems.map(item => ({
    product_id: item.id,
    quantity: item.quantity,
    customizations: item.customizations || {},
  }));
};

/**
 * Extract numeric price from string (e.g., "KES 350" -> 350)
 */
export const extractNumericPrice = (priceString) => {
  if (typeof priceString === 'number') return priceString;
  const match = priceString.match(/[\d,]+/);
  return match ? parseFloat(match[0].replace(/,/g, '')) : 0;
};

/**
 * Format price for display
 */
export const formatPrice = (price) => {
  return `KES ${typeof price === 'number' ? price.toFixed(0) : price}`;
};
