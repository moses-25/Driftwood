from extensions import db
from models import MenuItem

def seed_menu_data():
    """Seed the database with initial menu data"""
    
    # Check if data already exists
    if MenuItem.query.first():
        print("Menu data already exists, skipping seed...")
        return
    
    menu_items = [
        # Hot drinks
        MenuItem(
            name="Driftwood Espresso",
            description="Double shot, dark roast, with notes of cedar and dark chocolate.",
            price=350,
            category="hot",
            image_url="/images/hot1.jpg"
        ),
        MenuItem(
            name="Flat White",
            description="Velvety microfoam over a ristretto shot. Clean and bold.",
            price=420,
            category="hot",
            image_url="/images/hot2.jpg"
        ),
        MenuItem(
            name="Spiced Chai Latte",
            description="House-blended chai with cinnamon, cardamom, and steamed oat milk.",
            price=480,
            category="hot",
            image_url="/images/hot3.jpg"
        ),
        
        # Cold drinks
        MenuItem(
            name="Cold Brew",
            description="Steeped 18 hours. Smooth, low-acid, served over clear ice.",
            price=450,
            category="cold",
            image_url="/images/cold1.jpg"
        ),
        MenuItem(
            name="Iced Lavender Latte",
            description="House lavender syrup, espresso, whole milk over ice.",
            price=520,
            category="cold",
            image_url="/images/cold2.jpg"
        ),
        MenuItem(
            name="Mango Cold Foam",
            description="Cold brew topped with salted mango cold foam. Summer in a cup.",
            price=580,
            category="cold",
            image_url="/images/cold3.jpg"
        ),
        
        # Pastries
        MenuItem(
            name="Almond Croissant",
            description="Twice-baked with frangipane, toasted almonds, and powdered sugar.",
            price=380,
            category="pastries",
            image_url="/images/almond_croissant.jpg"
        ),
        MenuItem(
            name="Brown Butter Banana Bread",
            description="Moist, dense, with walnuts and a brown butter glaze.",
            price=350,
            category="pastries",
            image_url="/images/banana_bread.jpg"
        ),
        MenuItem(
            name="Matcha Scone",
            description="Ceremonial grade matcha with white chocolate chips and lemon zest.",
            price=400,
            category="pastries",
            image_url="/images/matcha_scone.jpg"
        ),
        
        # Specials
        MenuItem(
            name="Driftwood Signature",
            description="Espresso, coconut milk, cardamom, and a hint of rose. Our flagship.",
            price=600,
            category="specials",
            image_url="/images/special1.jpg"
        ),
        MenuItem(
            name="Fog Cutter",
            description="Cold brew, oat milk, sea salt caramel, and house cinnamon syrup.",
            price=620,
            category="specials",
            image_url="/images/special2.jpg"
        ),
        MenuItem(
            name="Ember & Oak",
            description="Smoked vanilla syrup, espresso, steamed whole milk, caramel drizzle.",
            price=650,
            category="specials",
            image_url="/images/special3.jpg"
        ),
        
        # Merchandise
        MenuItem(
            name="Driftwood Bucket Hat",
            description="A wide-brim black bucket hat with \"Driftwood cafe'\" embroidered in warm cream lettering.",
            price=2200,
            category="merch",
            tag="Bestseller",
            image_url="/images/merch1.jpg"
        ),
        MenuItem(
            name="Signature Canvas Tote",
            description="A sturdy all-black canvas tote bearing the full Driftwood Café identity.",
            price=1800,
            category="merch",
            tag="New",
            image_url="/images/merch2.jpg"
        ),
        MenuItem(
            name="Matte Black Ceramic Mug",
            description="A smooth matte-black ceramic mug with \"Driftwood cafe'\" printed in elegant cream-gold serif lettering.",
            price=1600,
            category="merch",
            image_url="/images/merch3.jpg"
        )
    ]
    
    for item in menu_items:
        db.session.add(item)
    
    try:
        db.session.commit()
        print(f"Successfully seeded {len(menu_items)} menu items!")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding menu data: {e}")

def init_database():
    """Initialize database with tables and seed data"""
    try:
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Seed menu data
        seed_menu_data()
        
    except Exception as e:
        print(f"Error initializing database: {e}")