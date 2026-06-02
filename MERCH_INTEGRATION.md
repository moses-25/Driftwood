# Merchandise Integration - Completed ✅

## Overview
Merchandise products are fully integrated into the Driftwood Café ordering system using **static data** (no database queries). Since merchandise items won't change, they're hardcoded in the frontend for faster loading and simpler management.

## Key Design Decision

### Static Data for Merch
- **Food/Beverages**: Fetched from backend database (can be updated by admin)
- **Merchandise**: Hardcoded in frontend static data (constant, won't change)

**Why?**
- ✅ Faster loading (no API calls)
- ✅ Simpler management (all merch in one file)
- ✅ No database overhead
- ✅ Merchandise inventory is fixed and won't change

## What Was Added

### Menu Page Update
Added **"Merch"** tab to the Menu page navigation, allowing customers to browse merchandise products.

**Menu Categories:**
1. Cold Brews
2. Hot Drinks
3. Pastries
4. Specials
5. **Merch** ← NEW

## Merchandise Products Available (6 items - Static Data)

All merchandise is defined in `/client/src/data/menuData.js`:

1. **Driftwood Bucket Hat** - KES 2,200
   - Wide-brim black bucket hat with embroidered logo
   - Tag: Bestseller
   - Subcategory: Accessories

2. **Signature Canvas Tote** - KES 1,800
   - Sturdy all-black canvas tote with café branding
   - Tag: New
   - Subcategory: Accessories

3. **Matte Black Ceramic Mug** - KES 1,600
   - Smooth matte-black ceramic mug with logo
   - Subcategory: Drinkware

4. **Driftwood Travel Tumbler** - KES 3,500
   - Insulated matte-black travel tumbler with flip-top lid
   - Tag: Bestseller
   - Subcategory: Drinkware

5. **Coffee Into Code Tee — Navy** - KES 2,800
   - Navy blue crew-neck tee with developer graphic
   - Subcategory: Apparel

6. **Coffee Into Code Tee — Grey** - KES 2,800
   - Heather grey crew-neck tee with code graphic
   - Tag: New
   - Subcategory: Apparel

## How It Works

### 1. Menu Display
- Users click the **"Merch"** tab on the Menu page
- Merchandise products display in the carousel
- Large featured image shows selected merch item
- Product details: name, description, price, image

### 2. Add to Cart
- Users can select quantity (1, 2, 3, etc.)
- Click "Add to Cart" button
- Merch items added to shopping cart

### 3. Checkout Process
- Merch items appear in cart alongside food/beverage items
- Same checkout flow applies:
  - Contact information
  - Delivery method (pickup/delivery)
  - Payment method (M-Pesa/Cash)
  - Order confirmation

### 4. Order Processing
- Backend treats merch as regular products
- Orders can contain mixed items (coffee + merch)
- Payment processing works identically
- Order tracking includes all items

## Technical Implementation

### Database Schema
```python
# server/models/menu_item.py
category = db.Column(db.String(50), nullable=False)
# Valid categories: 'hot', 'cold', 'pastries', 'specials', 'merch'
```

### Frontend Components
- **Menu.jsx**: Added "merch" to TABS array
- **MenuCard.jsx**: Displays merch items (reused component)
- **Cart**: Handles merch items (no changes needed)
- **Checkout**: Processes merch orders (no changes needed)

### Data Flow
```
Static Data (menuData.js)
        ↓
merchItems array (6 items)
        ↓
Menu Page: When activeTab === 'merch'
        ↓
Display in carousel + featured view
        ↓
No API calls needed!
```

### Code Implementation
```javascript
// Menu.jsx
const menuItems = useMemo(() => {
  // For merch category, always use static data
  if (activeTab === 'merch') {
    return merchItems; // Static data
  }
  
  // For other categories, use backend products
  if (backendProducts && backendProducts.length > 0) {
    return backendProducts; // From API
  }
  
  return staticMenuItems; // Fallback
}, [backendProducts, loading, error, activeTab]);
```

## Files Modified
- ✅ `/home/moses/workspace/COFFEE/Driftwood/client/src/pages/Menu.jsx` - Added merch tab + static data logic
- ✅ `/home/moses/workspace/COFFEE/Driftwood/client/src/data/menuData.js` - Updated merch items with `category: 'merch'`

## Files Verified (No Changes Needed)
- ✅ `/home/moses/workspace/COFFEE/Driftwood/client/src/components/MenuCard.jsx` - Works with merch items
- ✅ `/home/moses/workspace/COFFEE/Driftwood/client/src/hooks/useCart.jsx` - Handles merch items
- ✅ `/home/moses/workspace/COFFEE/Driftwood/client/src/pages/Checkout.jsx` - Processes merch orders

## Build Status
- ✅ Frontend builds successfully
- ✅ No compilation errors
- ✅ Merch tab displays correctly

## User Experience

### Navigation
1. User visits website
2. Scrolls to Menu section
3. Sees 5 category tabs: Cold Brews, Hot Drinks, Pastries, Specials, **Merch**
4. Clicks "Merch" tab
5. Browses merchandise products

### Shopping
1. User selects a merch item from carousel
2. Featured view shows large product image
3. User adjusts quantity
4. Clicks "Add to Cart"
5. Item added to shopping cart
6. User can continue shopping or checkout

### Mixed Orders
Users can order:
- ✅ Coffee only
- ✅ Merch only
- ✅ Coffee + Merch together
- ✅ Any combination of products

## Pricing
All merchandise prices are in Kenyan Shillings (KES):
- Bucket Hat: KES 2,200
- Canvas Tote: KES 1,800
- Ceramic Mug: KES 1,600

## Delivery
Merchandise follows the same delivery options:
- **Pickup**: Free (collect at café)
- **Delivery**: KES 399 delivery fee

## Payment
Merchandise can be paid for using:
- **M-Pesa**: Mobile money payment
- **Cash**: Pay on delivery/pickup

## Notes
- Merchandise images are stored in `/client/src/assets/Merch/`
- Backend serves merch products via standard product API
- No special handling needed for merch vs food items
- Cart, checkout, and payment systems work identically
- Order tracking includes all product types

## Future Enhancements (Optional)
1. Add more merchandise items to static data
2. Add size/color variants for apparel (in static data)
3. Add merchandise-specific filters (Apparel, Drinkware, Accessories)
4. Add bulk pricing for coffee-related merch
5. Add gift wrapping option for merch items

## How to Update Merchandise

Since merch uses static data, to add/update items:

1. Open `/client/src/data/menuData.js`
2. Edit the `merchItems` array
3. Add new items with this structure:
```javascript
{
  id: 'm7',                    // Unique ID
  name: 'Product Name',
  category: 'merch',           // Must be 'merch'
  subcategory: 'Accessories',  // Accessories/Drinkware/Apparel
  description: 'Product description...',
  price: 'KES 2,500',
  tag: 'Bestseller',           // or 'New' or null
  image: merchImage,           // Import image at top of file
}
```
4. Add product image to `/client/src/assets/Merch/`
5. Import image at top of `menuData.js`
6. Rebuild frontend: `npm run build`
