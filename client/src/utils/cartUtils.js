/**
 * Derive a stable line-item key from a product id + its customizations.
 * Two orders of the same product with different options become separate lines.
 * Orders with no customizations (or identical ones) are merged as before.
 */
export function makeCartItemId(productId, customizations) {
    if (!customizations || Object.keys(customizations).length === 0) {
        return String(productId)
    }
    // Sort keys so {milk:'oat',size:'large'} === {size:'large',milk:'oat'}
    const stable = JSON.stringify(customizations, Object.keys(customizations).sort())
    return `${productId}::${stable}`
}