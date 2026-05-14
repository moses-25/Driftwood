/**
 * Parse a price string — handles both "KES 450" and legacy "$3.50" formats → number
 */
export function parsePrice(priceStr) {
  const str = String(priceStr)
  // Legacy dollar format: "$3.50" → multiply by ~130 (approx KES rate) — but
  // we actually just want the numeric value so the cart math still works.
  // The display is always formatted as KES via formatPrice.
  return parseFloat(str.replace(/[^0-9.]/g, '')) || 0
}

/**
 * Format a number as a KES price string → "KES 450"
 */
export function formatPrice(amount) {
  return `KES ${Math.round(amount).toLocaleString('en-KE')}`
}

/**
 * Returns true if a price string is a legacy dollar price (e.g. "$3.50")
 */
export function isLegacyPrice(priceStr) {
  return String(priceStr).trim().startsWith('$')
}
