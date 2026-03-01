import random
import json

categories = [
    ('smartphone', 'Смартфоны', ['iPhone 17 Pro', 'Samsung Galaxy S26', 'Pixel 10 Pro', 'Xiaomi 16 Ultra', 'OnePlus 14', 'Sony Xperia 1 VIII', 'Asus ROG Phone 10', 'Nothing Phone (4)', 'Fold Z 8', 'Flip Z 8', 'Motorola Edge 60', 'Realme GT 7', 'Vivo X120', 'Oppo Find X9', 'Honor Magic 8']),
    ('laptop', 'Ноутбуки', ['MacBook Pro M5', 'Dell XPS 16 (2026)', 'Lenovo ThinkPad X1 Carbon Gen 14', 'Asus ZenBook Duo 2026', 'HP Spectre x360 15', 'Razer Blade 17 (2026)', 'MSI Titan GT78', 'Acer Swift X 16', 'Surface Laptop 7', 'Samsung Galaxy Book 5', 'LG Gram 17 (2026)', 'Alienware x16 R3', 'Framework Laptop 16', 'System76 Oryx Pro', 'Huawei MateBook X Pro 2026']),
    ('watch', 'Часы', ['Apple Watch Ultra 4', 'Galaxy Watch 8', 'Garmin Fenix 9', 'Pixel Watch 5', 'Xiaomi Watch S5', 'Huawei Watch 6 Pro', 'Amazfit GTR 6', 'Suunto 11 Peak', 'Fitbit Sense 4', 'Withings ScanWatch 3', 'Casio G-Shock Smart', 'Tag Heuer Connected E6', 'Fossil Gen 8', 'Mobvoi TicWatch Pro 7', 'Polar Vantage V4']),
    ('audio', 'Аудио', ['AirPods Max 2', 'Sony WH-1000XM6', 'Bose QC Ultra II', 'Sennheiser Momentum 5', 'Galaxy Buds 4 Pro', 'Pixel Buds Pro 3', 'JBL Tour One M3', 'Marshall Major VI', 'Bang & Olufsen H100', 'Sonos Ace 2', 'Devialet Gemini III', 'Audio-Technica ATH-M50xBT3', 'Beyerdynamic Amiron 2', 'Nothing Ear (4)', 'Anker Soundcore Liberty 5']),
    ('camera', 'Камеры', ['Sony A7 V', 'Canon EOS R5 Mark III', 'Nikon Z8 II', 'Fujifilm X-T6', 'Panasonic Lumix S2H', 'Leica Q4', 'Ricoh GR IV', 'GoPro Hero 14 Black', 'DJI Osmo Action 6', 'Insta360 X5', 'Blackmagic Pocket 8K', 'Hasselblad X3D', 'Olympus OM-1 Mark III', 'Sony ZV-E10 III', 'Canon PowerShot G7 X IV']),
    ('gaming', 'Гейминг', ['PlayStation 6', 'Xbox Series Z', 'Nintendo Switch 2', 'Steam Deck OLED 2', 'Asus ROG Ally 2', 'Lenovo Legion Go 2', 'MSI Claw 2', 'Logitech G Cloud 2', 'Ayaneo 3S', 'Pico 5 VR', 'Meta Quest 4', 'Valve Index 2', 'Razer Edge 5G', 'Nvidia Shield TV Pro 2026', 'Apple Vision Pro 2'])
]

images = {
    'smartphone': 'https://commons.wikimedia.org/wiki/Special:FilePath/IPhone_15_Pro_Vector.svg',
    'laptop': 'https://commons.wikimedia.org/wiki/Special:FilePath/MacBook_Pro_16_(M1_Pro,_2021)_-_Wikipedia_(cropped).jpg',
    'watch': 'https://commons.wikimedia.org/wiki/Special:FilePath/Apple_Watch_Ultra_49mm.svg',
    'audio': 'https://commons.wikimedia.org/wiki/Special:FilePath/Apple_AirPods_Max.jpg',
    'camera': 'https://commons.wikimedia.org/wiki/Special:FilePath/Canon_EOS_R5_(cropped).jpg',
    'gaming': 'https://commons.wikimedia.org/wiki/Special:FilePath/Playstation_5_being_displayed_in_electronics_retail_store_-_1.jpg'
}

slang_tags = {
    'smartphone': 'мобила,труба,сотик,звонилка,кирпич,смарт,телефон,флагман,камерофон',
    'laptop': 'ноут,пекарня,лэптоп,машина,комп,бук,ультрабук',
    'watch': 'котлы,часики,умные часы,браслет,фитнес,трекер',
    'audio': 'уши,наушники,затычки,лопухи,звук,басы,музыка',
    'camera': 'фотик,зеркалка,беззеркалка,мыльница,тушка,объектив,линза',
    'gaming': 'консоль,приставка,плойка,ящик,свич,геймпад,джойстик,vr,виар'
}

descriptions = [
    "Невероятная производительность в 2026 году. Чип нового поколения обеспечивает молниеносную скорость работы в любых приложениях.",
    "Идеальный выбор для профессионалов и геймеров. Поддержка AI-функций на аппаратном уровне открывает новые горизонты творчества.",
    "Лучшее соотношение цены и качества. Хит продаж 2026 года благодаря сбалансированным характеристикам и стильному дизайну.",
    "Стильный дизайн и автономность до 48 часов. Будущее уже здесь - устройство, которое понимает вас с полуслова.",
    "Максимальная комплектация. Гарантия 2 года. Эксклюзивные материалы корпуса и премиальная сборка."
]

def generate_specs(category):
    specs = {}
    if category == 'smartphone':
        specs = {
            'screen': f"{random.choice(['6.1', '6.7', '6.9'])}\" OLED 144Hz",
            'cpu': f"Snapdragon 8 Gen {random.randint(4,5)} / A{random.randint(18,19)} Pro",
            'camera': f"{random.choice(['50', '108', '200'])} MP Main",
            'battery': f"{random.randint(4000, 6000)} mAh"
        }
    elif category == 'laptop':
        specs = {
            'screen': f"{random.choice(['14', '16', '13'])}\" Mini-LED",
            'cpu': f"M{random.randint(4,5)} Max / i{random.randint(7,9)} Ultra",
            'ram': f"{random.choice(['16', '32', '64'])} GB",
            'ssd': f"{random.choice(['512 GB', '1 TB', '2 TB'])}"
        }
    elif category == 'watch':
        specs = {
            'screen': "49mm Always-On",
            'battery': "72h",
            'water': "100m WR",
            'sensors': "HR, ECG, O2"
        }
    elif category == 'audio':
        specs = {
            'anc': "Active Noise Cancel",
            'battery': "30h Playback",
            'driver': "40mm Dynamic",
            'conn': "BT 6.0"
        }
    elif category == 'camera':
        specs = {
            'sensor': "Full Frame 45MP",
            'video': "8K 60fps RAW",
            'iso': "100-102400",
            'stabil': "5-axis IBIS"
        }
    elif category == 'gaming':
        specs = {
            'gpu': "12 TFLOPS RDNA 4",
            'ssd': "2 TB Gen5 NVMe",
            'output': "8K 120Hz",
            'ram': "24 GB GDDR7"
        }
    return json.dumps(specs, ensure_ascii=False)

print("DROP TABLE IF EXISTS products;")
print("DROP TABLE IF EXISTS users;")
print("DROP TABLE IF EXISTS orders;")
print("DROP TABLE IF EXISTS wishlist;")

print("CREATE TABLE products (id SERIAL PRIMARY KEY, name TEXT, category TEXT, price INTEGER, description TEXT, image_url TEXT, tags TEXT, specs TEXT);")
print("CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL);")
print("CREATE TABLE orders (id SERIAL PRIMARY KEY, user_id INTEGER, items TEXT, total INTEGER, status TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")
print("CREATE TABLE wishlist (id SERIAL PRIMARY KEY, user_id INTEGER, product_id INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")

for cat_key, cat_name, items in categories:
    for item in items:
        price = random.randint(30000, 250000)
        desc = random.choice(descriptions)
        img = images[cat_key]
        tags = f"{cat_key},{cat_name.lower()},{item.lower()},{slang_tags[cat_key]}"
        specs_json = generate_specs(cat_key)
        
        # Escape single quotes in names
        item_safe = item.replace("'", "''")
        
        print(f"INSERT INTO products (name, category, price, description, image_url, tags, specs) VALUES ('{item_safe}', '{cat_key}', {price}, '{desc}', '{img}', '{tags}', '{specs_json}');")
