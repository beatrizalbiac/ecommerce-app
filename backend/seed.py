# To fill the db with some example products so they don't have to be created each time anything wants to be tested. The content of the products was AI generated

from sqlmodel import Session, select
from app.db import engine
from app.models.users import User
from app.models.orders import Order
from app.models.order_items import OrderItem
from app.models.products import Product

def sample_products():
    products = [
        # ========== SMARTPHONES & TABLETS ==========
        Product(
            title="iPhone 15 Pro",
            slug="iphone-15-pro",
            description="The latest iPhone with A17 Pro chip and 48MP camera. Super Retina XDR display with 6.1-inch screen.",
            price_cents=119900,
            currency="EUR",
            stock=50
        ),
        Product(
            title="iPhone 15",
            slug="iphone-15",
            description="Standard iPhone 15 with A16 Bionic chip. Excellent camera and battery life.",
            price_cents=89900,
            currency="EUR",
            stock=75
        ),
        Product(
            title="iPhone 14 Pro Max",
            slug="iphone-14-pro-max",
            description="Previous generation flagship iPhone with 6.7-inch display and Dynamic Island.",
            price_cents=109900,
            currency="EUR",
            stock=30
        ),
        Product(
            title="Samsung Galaxy S24 Ultra",
            slug="samsung-s24-ultra",
            description="Premium Android smartphone with S Pen included, 200MP camera and Dynamic AMOLED 2X display.",
            price_cents=139900,
            currency="EUR",
            stock=45
        ),
        Product(
            title="Samsung Galaxy S24",
            slug="samsung-s24",
            description="Flagship Samsung phone with AI features and excellent camera system.",
            price_cents=89900,
            currency="EUR",
            stock=60
        ),
        Product(
            title="Google Pixel 8 Pro",
            slug="google-pixel-8-pro",
            description="Google's flagship phone with Tensor G3 chip and advanced AI photography features.",
            price_cents=99900,
            currency="EUR",
            stock=40
        ),
        Product(
            title="iPad Pro 12.9",
            slug="ipad-pro-12-9",
            description="Professional tablet with M2 chip, Liquid Retina XDR display and Apple Pencil compatibility.",
            price_cents=139900,
            currency="EUR",
            stock=25
        ),
        Product(
            title="iPad Air",
            slug="ipad-air",
            description="Lightweight tablet with M1 chip, perfect balance of performance and portability.",
            price_cents=69900,
            currency="EUR",
            stock=50
        ),
        Product(
            title="Samsung Galaxy Tab S9",
            slug="samsung-galaxy-tab-s9",
            description="Premium Android tablet with S Pen included and water resistance.",
            price_cents=79900,
            currency="EUR",
            stock=35
        ),
        
        # ========== LAPTOPS & COMPUTERS ==========
        Product(
            title="MacBook Air M3",
            slug="macbook-air-m3",
            description="Ultra-lightweight laptop with Apple's powerful M3 chip. 13-inch display with up to 18 hours of battery life.",
            price_cents=129900,
            currency="EUR",
            stock=30
        ),
        Product(
            title="MacBook Pro 14 M3",
            slug="macbook-pro-14-m3",
            description="Professional laptop with M3 Pro chip, perfect for creative work and demanding tasks.",
            price_cents=219900,
            currency="EUR",
            stock=20
        ),
        Product(
            title="MacBook Pro 16 M3 Max",
            slug="macbook-pro-16-m3-max",
            description="Ultimate MacBook with M3 Max chip, 16-inch display for professional workflows.",
            price_cents=349900,
            currency="EUR",
            stock=15
        ),
        Product(
            title="Dell XPS 15",
            slug="dell-xps-15",
            description="Premium Windows laptop with Intel Core i9, OLED display and professional build quality.",
            price_cents=189900,
            currency="EUR",
            stock=25
        ),
        Product(
            title="Lenovo ThinkPad X1 Carbon",
            slug="lenovo-thinkpad-x1-carbon",
            description="Business laptop with legendary keyboard, lightweight carbon fiber chassis.",
            price_cents=169900,
            currency="EUR",
            stock=30
        ),
        Product(
            title="ASUS ROG Zephyrus G14",
            slug="asus-rog-zephyrus-g14",
            description="Compact gaming laptop with AMD Ryzen 9 and RTX 4060, excellent for gaming and creative work.",
            price_cents=179900,
            currency="EUR",
            stock=20
        ),
        Product(
            title="Microsoft Surface Laptop 5",
            slug="microsoft-surface-laptop-5",
            description="Elegant Windows laptop with touchscreen display and premium aluminum design.",
            price_cents=149900,
            currency="EUR",
            stock=35
        ),
        
        # ========== AUDIO (Headphones, Earbuds, Speakers) ==========
        Product(
            title="AirPods Pro 2",
            slug="airpods-pro-2",
            description="Wireless earbuds with active noise cancellation and personalized spatial audio.",
            price_cents=27900,
            currency="EUR",
            stock=100
        ),
        Product(
            title="AirPods Max",
            slug="airpods-max",
            description="Over-ear headphones with high-fidelity audio, active noise cancellation and premium build.",
            price_cents=59900,
            currency="EUR",
            stock=40
        ),
        Product(
            title="Sony WH-1000XM5",
            slug="sony-wh-1000xm5",
            description="Over-ear headphones with industry-leading noise cancellation. 30 hours of battery life.",
            price_cents=39900,
            currency="EUR",
            stock=75
        ),
        Product(
            title="Sony WF-1000XM5",
            slug="sony-wf-1000xm5",
            description="Premium wireless earbuds with exceptional noise cancellation and sound quality.",
            price_cents=29900,
            currency="EUR",
            stock=60
        ),
        Product(
            title="Bose QuietComfort Ultra",
            slug="bose-quietcomfort-ultra",
            description="Flagship headphones from Bose with immersive audio and world-class noise cancellation.",
            price_cents=44900,
            currency="EUR",
            stock=50
        ),
        Product(
            title="JBL Flip 6",
            slug="jbl-flip-6",
            description="Portable Bluetooth speaker with powerful bass, waterproof design for outdoor use.",
            price_cents=12900,
            currency="EUR",
            stock=120
        ),
        Product(
            title="Sonos Era 300",
            slug="sonos-era-300",
            description="Premium smart speaker with spatial audio and multi-room capabilities.",
            price_cents=49900,
            currency="EUR",
            stock=40
        ),
        Product(
            title="Beats Studio Pro",
            slug="beats-studio-pro",
            description="Wireless headphones with active noise cancellation and USB-C audio.",
            price_cents=34900,
            currency="EUR",
            stock=65
        ),
        
        # ========== GAMING ==========
        Product(
            title="PlayStation 5",
            slug="playstation-5",
            description="Next-generation gaming console with 4K graphics, ultra-fast SSD and DualSense controller.",
            price_cents=54900,
            currency="EUR",
            stock=20
        ),
        Product(
            title="PlayStation 5 Digital Edition",
            slug="playstation-5-digital",
            description="All-digital PS5 console without disc drive, same powerful gaming experience.",
            price_cents=44900,
            currency="EUR",
            stock=25
        ),
        Product(
            title="Xbox Series X",
            slug="xbox-series-x",
            description="Microsoft's flagship gaming console with 4K/120fps gaming and Game Pass compatibility.",
            price_cents=54900,
            currency="EUR",
            stock=30
        ),
        Product(
            title="Nintendo Switch OLED",
            slug="nintendo-switch-oled",
            description="Hybrid gaming console with 7-inch OLED screen. Play at home or on the go.",
            price_cents=34900,
            currency="EUR",
            stock=60
        ),
        Product(
            title="Steam Deck OLED",
            slug="steam-deck-oled",
            description="Handheld gaming PC with OLED display, play your Steam library anywhere.",
            price_cents=56900,
            currency="EUR",
            stock=35
        ),
        Product(
            title="Meta Quest 3",
            slug="meta-quest-3",
            description="Advanced VR headset with mixed reality capabilities and standalone gaming.",
            price_cents=54900,
            currency="EUR",
            stock=40
        ),
        
        # ========== GAMING ACCESSORIES ==========
        Product(
            title="Razer DeathAdder V3 Pro",
            slug="razer-deathadder-v3-pro",
            description="Professional wireless gaming mouse with exceptional precision and ergonomics.",
            price_cents=14900,
            currency="EUR",
            stock=80
        ),
        Product(
            title="Logitech G Pro X Superlight",
            slug="logitech-g-pro-x-superlight",
            description="Ultra-lightweight wireless gaming mouse trusted by esports professionals.",
            price_cents=15900,
            currency="EUR",
            stock=70
        ),
        Product(
            title="SteelSeries Arctis Nova Pro Wireless",
            slug="steelseries-arctis-nova-pro",
            description="Premium gaming headset with active noise cancellation and dual battery system.",
            price_cents=34900,
            currency="EUR",
            stock=45
        ),
        Product(
            title="Corsair K70 RGB",
            slug="corsair-k70-rgb",
            description="Mechanical gaming keyboard with Cherry MX switches and customizable RGB lighting.",
            price_cents=16900,
            currency="EUR",
            stock=55
        ),
        
        # ========== PRODUCTIVITY & PERIPHERALS ==========
        Product(
            title="Logitech MX Master 3S",
            slug="logitech-mx-master-3s",
            description="High-precision ergonomic wireless mouse. Perfect for productivity workflows.",
            price_cents=10900,
            currency="EUR",
            stock=150
        ),
        Product(
            title="Logitech MX Keys",
            slug="logitech-mx-keys",
            description="Wireless keyboard with smart illumination and comfortable typing experience.",
            price_cents=11900,
            currency="EUR",
            stock=120
        ),
        Product(
            title="Apple Magic Keyboard",
            slug="apple-magic-keyboard",
            description="Wireless keyboard with rechargeable battery, perfect companion for Mac.",
            price_cents=9900,
            currency="EUR",
            stock=100
        ),
        Product(
            title="Apple Magic Trackpad",
            slug="apple-magic-trackpad",
            description="Wireless trackpad with Multi-Touch gestures and Force Touch technology.",
            price_cents=14900,
            currency="EUR",
            stock=85
        ),
        Product(
            title="Logitech Webcam C920",
            slug="logitech-webcam-c920",
            description="Full HD 1080p webcam with autofocus, perfect for video calls and streaming.",
            price_cents=7900,
            currency="EUR",
            stock=200
        ),
        Product(
            title="Blue Yeti Microphone",
            slug="blue-yeti-microphone",
            description="Professional USB microphone for streaming, podcasting and content creation.",
            price_cents=12900,
            currency="EUR",
            stock=90
        ),
        
        # ========== SMART HOME & WEARABLES ==========
        Product(
            title="Apple Watch Series 9",
            slug="apple-watch-series-9",
            description="Advanced smartwatch with health tracking, fitness features and always-on display.",
            price_cents=44900,
            currency="EUR",
            stock=70
        ),
        Product(
            title="Apple Watch Ultra 2",
            slug="apple-watch-ultra-2",
            description="Rugged smartwatch for extreme sports with titanium case and extended battery.",
            price_cents=89900,
            currency="EUR",
            stock=30
        ),
        Product(
            title="Samsung Galaxy Watch 6",
            slug="samsung-galaxy-watch-6",
            description="Android smartwatch with comprehensive health tracking and sleep monitoring.",
            price_cents=34900,
            currency="EUR",
            stock=60
        ),
        Product(
            title="Fitbit Charge 6",
            slug="fitbit-charge-6",
            description="Fitness tracker with heart rate monitoring, GPS and 7-day battery life.",
            price_cents=15900,
            currency="EUR",
            stock=110
        ),
        Product(
            title="Amazon Echo Dot 5th Gen",
            slug="amazon-echo-dot-5",
            description="Compact smart speaker with Alexa, perfect for any room in your home.",
            price_cents=5900,
            currency="EUR",
            stock=250
        ),
        Product(
            title="Google Nest Hub 2nd Gen",
            slug="google-nest-hub-2",
            description="Smart display with Google Assistant, touchscreen and sleep tracking.",
            price_cents=9900,
            currency="EUR",
            stock=140
        ),
        Product(
            title="Ring Video Doorbell",
            slug="ring-video-doorbell",
            description="Smart doorbell with 1080p video, two-way talk and motion detection.",
            price_cents=9900,
            currency="EUR",
            stock=130
        ),
        
        # ========== E-READERS & ACCESSORIES ==========
        Product(
            title="Kindle Paperwhite",
            slug="kindle-paperwhite",
            description="E-reader with 6.8-inch display and adjustable warm light for comfortable reading.",
            price_cents=14900,
            currency="EUR",
            stock=80
        ),
        Product(
            title="Kindle Oasis",
            slug="kindle-oasis",
            description="Premium e-reader with 7-inch display, page-turn buttons and waterproof design.",
            price_cents=24900,
            currency="EUR",
            stock=50
        ),
        Product(
            title="Kobo Libra 2",
            slug="kobo-libra-2",
            description="E-reader with ComfortLight PRO and support for multiple ebook formats.",
            price_cents=17900,
            currency="EUR",
            stock=65
        ),
        
        # ========== CAMERAS & PHOTOGRAPHY ==========
        Product(
            title="GoPro Hero 12 Black",
            slug="gopro-hero-12-black",
            description="Action camera with 5.3K video, waterproof design and HyperSmooth stabilization.",
            price_cents=44900,
            currency="EUR",
            stock=55
        ),
        Product(
            title="DJI Mini 3 Pro",
            slug="dji-mini-3-pro",
            description="Compact drone with 4K HDR video, 34-minute flight time and obstacle avoidance.",
            price_cents=74900,
            currency="EUR",
            stock=40
        ),
        Product(
            title="Fujifilm Instax Mini 12",
            slug="fujifilm-instax-mini-12",
            description="Instant camera with automatic exposure and close-up mode for fun photography.",
            price_cents=7900,
            currency="EUR",
            stock=150
        ),
        
        # ========== STORAGE & ACCESSORIES ==========
        Product(
            title="Samsung T7 Portable SSD 1TB",
            slug="samsung-t7-1tb",
            description="Ultra-fast portable SSD with USB 3.2 Gen 2 for quick file transfers.",
            price_cents=10900,
            currency="EUR",
            stock=180
        ),
        Product(
            title="SanDisk Extreme Portable SSD 2TB",
            slug="sandisk-extreme-2tb",
            description="Rugged portable SSD with IP55 rating, perfect for outdoor professionals.",
            price_cents=17900,
            currency="EUR",
            stock=120
        ),
        Product(
            title="Anker PowerCore 20000mAh",
            slug="anker-powercore-20000",
            description="High-capacity portable charger with fast charging for phones and tablets.",
            price_cents=5900,
            currency="EUR",
            stock=300
        ),
        Product(
            title="Apple USB-C Cable 2m",
            slug="apple-usb-c-cable-2m",
            description="Durable USB-C charging cable compatible with iPhone 15 and later.",
            price_cents=2900,
            currency="EUR",
            stock=400
        ),
        Product(
            title="Belkin 3-in-1 Wireless Charger",
            slug="belkin-3-in-1-charger",
            description="Charge iPhone, Apple Watch and AirPods simultaneously with MagSafe.",
            price_cents=14900,
            currency="EUR",
            stock=90
        ),
    ]

    with Session(engine) as session:
        sel = select(Product)
        existing = session.exec(sel).first()

        if existing:
            print("Already exists. Skipping...")
            return
        
        for i in products:
            session.add(i)

        session.commit()
        print("Products added")

if __name__ == "__main__" :
    sample_products()