/**
 * Parse price string to number
 * Handles formats like "KES 350", "350", "$3.50", etc.
 */
export const parsePrice = (priceString) => {
  if (typeof priceString === 'number' && !Number.isNaN(priceString)) return priceString;
  
  // Remove currency symbols and commas, extract numbers
  const match = String(priceString).match(/[\d,]+\.?\d*/);
  if (!match) return 0;
  const parsed = parseFloat(match[0].replace(/,/g, ''));
  return Number.isNaN(parsed) ? 0 : parsed;
};

/**
 * Format number as price
 */
export const formatPrice = (price) => {
  return `KES ${Math.round(price).toLocaleString('en-KE')}`;
};

/**
 * Calculate total from cart items
 */
export const calculateTotal = (items) => {
  return items.reduce((sum, item) => {
    const price = parsePrice(item.price);
    const quantity = item.quantity || 1;
    return sum + (price * quantity);
  }, 0);
};

/**
 * Calculate tax (16% VAT in Kenya)
 */
export const calculateTax = (subtotal, taxRate = 0.16) => {
  return subtotal * taxRate;
};

/**
 * Calculate grand total with delivery and tax
 */
export const calculateGrandTotal = (subtotal, deliveryFee = 0, taxRate = 0.16) => {
  const tax = calculateTax(subtotal, taxRate);
  return subtotal + deliveryFee + tax;
};
