from extensions import db
from models.category import Category
from models.product import Product


def seed_categories():
    if Category.query.first():
        print("Categories already exist, skipping...")
        return

    categories = [
        Category(name="Hot Drinks", description="Freshly brewed hot beverages", sort_order=1, image_url="/images/hot.jpg"),
        Category(name="Cold Drinks", description="Refreshing cold beverages", sort_order=2, image_url="/images/cold.jpg"),
        Category(name="Pastries", description="Freshly baked pastries and treats", sort_order=3, image_url="/images/pastries.jpg"),
        Category(name="Specials", description="Seasonal and signature specials", sort_order=4, image_url="/images/specials.jpg"),
        Category(name="Merchandise", description="Driftwood Café merchandise", sort_order=5, image_url="/images/merch.jpg"),
    ]

    for cat in categories:
        db.session.add(cat)

    db.session.commit()
    print(f"Seeded {len(categories)} categories")


def seed_products():
    if Product.query.first():
        print("Products already exist, skipping...")
        return

    cats = {c.name: c.id for c in Category.query.all()}

    products = [
        # Hot Drinks
        Product(name="Driftwood Espresso", description="Double shot, dark roast, with notes of cedar and dark chocolate.",
                price=350, category_id=cats["Hot Drinks"], image_url="/images/hot1.jpg", tag="Bestseller",
                preparation_time=3, calories=5),
        Product(name="Flat White", description="Velvety microfoam over a ristretto shot. Clean and bold.",
                price=420, category_id=cats["Hot Drinks"], image_url="/images/hot2.jpg",
                preparation_time=5, calories=120),
        Product(name="Spiced Chai Latte", description="House-blended chai with cinnamon, cardamom, and steamed oat milk.",
                price=480, category_id=cats["Hot Drinks"], image_url="/images/hot3.jpg", tag="Featured",
                preparation_time=5, calories=180),

        # Cold Drinks
        Product(name="Cold Brew", description="Steeped 18 hours. Smooth, low-acid, served over clear ice.",
                price=450, category_id=cats["Cold Drinks"], image_url="/images/cold1.jpg",
                preparation_time=2, calories=10),
        Product(name="Iced Lavender Latte", description="House lavender syrup, espresso, whole milk over ice.",
                price=520, category_id=cats["Cold Drinks"], image_url="/images/cold2.jpg",
                preparation_time=4, calories=150),
        Product(name="Mango Cold Foam", description="Cold brew topped with salted mango cold foam. Summer in a cup.",
                price=580, category_id=cats["Cold Drinks"], image_url="/images/cold3.jpg", tag="Seasonal",
                preparation_time=4, calories=130),

        # Pastries
        Product(name="Almond Croissant", description="Twice-baked with frangipane, toasted almonds, and powdered sugar.",
                price=380, category_id=cats["Pastries"], image_url="/images/almond_croissant.jpg",
                preparation_time=1, calories=320, track_inventory=False),
        Product(name="Brown Butter Banana Bread", description="Moist, dense, with walnuts and a brown butter glaze.",
                price=350, category_id=cats["Pastries"], image_url="/images/banana_bread.jpg",
                preparation_time=1, calories=280, track_inventory=False),
        Product(name="Matcha Scone", description="Ceremonial grade matcha with white chocolate chips and lemon zest.",
                price=400, category_id=cats["Pastries"], image_url="/images/matcha_scone.jpg",
                preparation_time=1, calories=260, track_inventory=False),

        # Specials
        Product(name="Driftwood Signature", description="Espresso, coconut milk, cardamom, and a hint of rose. Our flagship.",
                price=600, category_id=cats["Specials"], image_url="/images/special1.jpg", tag="Bestseller",
                preparation_time=6, calories=160),
        Product(name="Fog Cutter", description="Cold brew, oat milk, sea salt caramel, and house cinnamon syrup.",
                price=620, category_id=cats["Specials"], image_url="/images/special2.jpg", tag="Featured",
                preparation_time=5, calories=200),
        Product(name="Ember & Oak", description="Smoked vanilla syrup, espresso, steamed whole milk, caramel drizzle.",
                price=650, category_id=cats["Specials"], image_url="/images/special3.jpg",
                preparation_time=6, calories=220),

        # Merchandise
        Product(name="Driftwood Bucket Hat", description='A wide-brim black bucket hat with "Driftwood cafe\'" embroidered in warm cream lettering.',
                price=2200, category_id=cats["Merchandise"], image_url="/images/merch1.jpg", tag="Bestseller",
                track_inventory=False),
        Product(name="Signature Canvas Tote", description="A sturdy all-black canvas tote bearing the full Driftwood Café identity.",
                price=1800, category_id=cats["Merchandise"], image_url="/images/merch2.jpg", tag="New",
                track_inventory=False),
        Product(name="Matte Black Ceramic Mug", description='A smooth matte-black ceramic mug with "Driftwood cafe\'" printed in elegant cream-gold serif lettering.',
                price=1600, category_id=cats["Merchandise"], image_url="/images/merch3.jpg",
                track_inventory=False),
    ]

    for p in products:
        db.session.add(p)

    db.session.commit()
    print(f"Seeded {len(products)} products")


def seed_all():
    seed_categories()
    seed_products()
