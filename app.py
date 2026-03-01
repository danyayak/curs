import os
import re
from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from fuzzywuzzy import process, fuzz
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_demo_only' # In production use random bytes

# Database Configuration
db_user = os.environ.get('DB_USER', 'shop_user')
db_password = os.environ.get('DB_PASSWORD', 'shop_password')
db_host = os.environ.get('DB_HOST', 'db')
db_port = os.environ.get('DB_PORT', '5432')
db_name = os.environ.get('DB_NAME', 'shop')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    price = db.Column(db.Integer)
    description = db.Column(db.String)
    image_url = db.Column(db.String)
    tags = db.Column(db.String)
    specs = db.Column(db.String)

    def to_dict(self):
        import json
        specs_dict = {}
        if self.specs:
            try:
                specs_dict = json.loads(self.specs)
            except:
                pass
                
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': self.price,
            'description': self.description,
            'image_url': self.image_url,
            'tags': self.tags,
            'specs': specs_dict
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    items = db.Column(db.String)
    total = db.Column(db.Integer)
    status = db.Column(db.String)
    date = db.Column(db.DateTime, server_default=db.func.now())

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# NLP Logic
def parse_query(text):
    text = text.lower()
    filters = {}
    
    # 1. Category
    if re.search(r'ноут|laptop|пекарня|лэптоп|бук|комп|пк', text):
        filters['category'] = 'laptop'
    elif re.search(r'смартфон|телефон|smartphone|phone|мобила|труба|сотик|звонилка|кирпич|айфон|iphone|андроид|android|андройд', text):
        filters['category'] = 'smartphone'
    elif re.search(r'часы|watch|котлы|браслет|трекер', text):
        filters['category'] = 'watch'
    elif re.search(r'наушники|audio|sound|уши|затычки|звук|музыка|гарнитура', text):
        filters['category'] = 'audio'
    elif re.search(r'камера|camera|фотик|зеркалка|фото', text):
        filters['category'] = 'camera'
    elif re.search(r'гейминг|gaming|игр|консоль|приставка|плойка|xbox|playstation|ps5|ps6', text):
        filters['category'] = 'gaming'

        
    # 2. Price
    price_match = re.search(r'(до|дешевле|меньше)\s*(\d+)\s*(к|тыс)?', text)
    if price_match:
        amount = int(price_match.group(2))
        multiplier = price_match.group(3)
        if multiplier and (multiplier == 'к' or multiplier == 'тыс'):
            amount *= 1000
        filters['max_price'] = amount
        
    # 3. Tags
    found_tags = []
    tag_map = {
        'gaming': ['игровой', 'геймерский', 'gaming', 'гейминг'],
        'ultrabook': ['ультрабук', 'легкий', 'ultrabook'],
        'apple': ['apple', 'эпл', 'айфон', 'iphone', 'macbook', 'макбук', 'ipad', 'watch'],
        'android': ['android', 'андроид', 'андройд'],
        'ios': ['ios'],
        'budget': ['бюджетный', 'недорогой', 'дешевый', 'выгодно'],
        'flagship': ['флагман', 'топовый', 'мощный', 'хит']
    }
    
    for tag_key, synonyms in tag_map.items():
        for synonym in synonyms:
            if synonym in text:
                found_tags.append(tag_key)
                break
    
    if found_tags:
        filters['tags'] = found_tags
        
    return filters

# Routes
@app.route('/')
def index():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    
    # Get 2026 novelties (random selection for now, or latest added)
    novelties = Product.query.order_by(Product.id.desc()).limit(8).all()
    return render_template('index.html', user=user, novelties=novelties)

@app.route('/catalog')
def catalog():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    
    category = request.args.get('category')
    search = request.args.get('search')
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    sort = request.args.get('sort')
    
    query = Product.query
    if category:
        query = query.filter(Product.category == category)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(or_(Product.name.ilike(search_term), Product.tags.ilike(search_term)))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
        
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'newest':
        query = query.order_by(Product.id.desc())
    else:
        # Default: popular (simulated by random or id)
        query = query.order_by(Product.id.asc())

    products = query.all()
    
    wishlist_ids = []
    if user:
        wishlist_items = Wishlist.query.filter_by(user_id=user.id).all()
        wishlist_ids = [item.product_id for item in wishlist_items]
        
    return render_template('catalog.html', user=user, products=products, active_category=category, wishlist_ids=wishlist_ids)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    
    product = Product.query.get_or_404(product_id)
    
    import json
    try:
        specs = json.loads(product.specs)
    except:
        specs = {}
        
    wishlist_ids = []
    if user:
        wishlist_items = Wishlist.query.filter_by(user_id=user.id).all()
        wishlist_ids = [item.product_id for item in wishlist_items]

    return render_template('product.html', user=user, product=product, specs=specs, wishlist_ids=wishlist_ids)

@app.route('/cart')
def cart():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('cart.html', user=user)

@app.route('/checkout')
def checkout_page():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('checkout.html', user=user)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
        
    user = User.query.get(session['user_id'])
    if not user:
        session.pop('user_id', None)
        return redirect(url_for('index'))
        
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.date.desc()).all()
    return render_template('profile.html', user=user, orders=orders)

@app.route('/api/search_catalog')
def search_catalog():
    query_text = request.args.get('q', '')
    if not query_text:
        return jsonify([])
        
    # Use NLP logic for smarter search
    filters = parse_query(query_text)
    query = Product.query
    
    if 'category' in filters:
        query = query.filter(Product.category == filters['category'])
    if 'max_price' in filters:
        query = query.filter(Product.price <= filters['max_price'])
        
    products = query.all()
    
    # Fuzzy match if no strict filters or to refine
    if products:
        scored = []
        for p in products:
            score = fuzz.partial_ratio(query_text.lower(), f"{p.name.lower()} {p.tags.lower()}")
            scored.append((score, p))
        scored.sort(key=lambda x: x[0], reverse=True)
        products = [p for s, p in scored if s > 40]
        
    return jsonify([p.to_dict() for p in products])


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Заполните все поля'}), 400
        
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Пользователь уже существует'}), 400
        
    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    
    session['user_id'] = new_user.id
    return jsonify({'success': True, 'username': username})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({'success': True, 'username': username})
        
    return jsonify({'error': 'Неверный логин или пароль'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'success': True})

@app.route('/api/wishlist/toggle', methods=['POST'])
def toggle_wishlist():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    product_id = data.get('product_id')
    user_id = session['user_id']
    
    item = Wishlist.query.filter_by(user_id=user_id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        action = 'removed'
    else:
        new_item = Wishlist(user_id=user_id, product_id=product_id)
        db.session.add(new_item)
        action = 'added'
    db.session.commit()
    return jsonify({'success': True, 'action': action})

@app.route('/api/checkout', methods=['POST'])
def checkout():
    # Mock payment processing
    data = request.json
    if not data.get('card_number') or not data.get('cvc'):
         return jsonify({'error': 'Неверные данные карты'}), 400
    
    if 'user_id' in session:
        # Save order
        new_order = Order(
            user_id=session['user_id'],
            items=str(data.get('items', [])), # In real app, use JSON type
            total=data.get('total', 0),
            status='Оплачен'
        )
        db.session.add(new_order)
        db.session.commit()
    
    return jsonify({'success': True, 'message': 'Оплата прошла успешно!'})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'reply': 'Пожалуйста, введите запрос.', 'products': []})
        
    # Basic conversation
    lower_msg = user_message.lower()
    
    # Ignore very short queries unless they are specific words
    if len(lower_msg) < 3:
         return jsonify({'reply': 'Пожалуйста, уточните запрос. Слишком коротко 🧐', 'products': []})

    if re.search(r'^(привет|здравствуй|hello|hi|ку|сап)', lower_msg):
        return jsonify({'reply': 'Привет! Я помогу подобрать технику. Что ищем?', 'products': []})
    
    if re.search(r'^(пока|до свидания|bye)', lower_msg):
        return jsonify({'reply': 'До связи! Заходите еще.', 'products': []})
        
    if re.search(r'^(спасибо|спс|thanks)', lower_msg):
        return jsonify({'reply': 'Рад помочь! 😊', 'products': []})

    filters = parse_query(user_message)
    query = Product.query
    
    if 'category' in filters:
        query = query.filter(Product.category == filters['category'])
        
    if 'max_price' in filters:
        query = query.filter(Product.price <= filters['max_price'])

    # Handle Android specifically
    if 'android' in filters.get('tags', []):
        # Filter out Apple products if Android is requested
        # Check for 'apple', 'iphone', 'ios' in tags to be sure
        query = query.filter(
            ~Product.tags.ilike('%apple%'),
            ~Product.tags.ilike('%iphone%'),
            ~Product.tags.ilike('%ios%')
        )
        # Ensure category is smartphone if not set (optional but safer)
        if 'category' not in filters:
             query = query.filter(Product.category == 'smartphone')
             
    # General tag filtering (inclusive) - if Android is present, we already handled strict filtering above
    # but we still want to match other tags
    if 'tags' in filters:
        # We need to filter in python because tags are a string
        # Or better: use ILIKE for each tag
        pass 
        
    products = query.all()
    
    # Filter by tags if any found (Python side for CSV tags)
    if 'tags' in filters:
        filtered_products = []
        for p in products:
            p_tags = [t.strip() for t in p.tags.split(',')]
            # Check if any of the requested tags match
            # Special logic for Android: we already filtered DB to exclude Apple, 
            # but we should ensure we don't accidentally filter OUT androids if 'android' is the only tag
            
            match = False
            for req_tag in filters['tags']:
                if req_tag == 'android':
                    # If we asked for android, and we already excluded Apple, 
                    # we basically accept all remaining smartphones that aren't obviously something else?
                    # Or we check if 'android' or 'smartphone' is in tags?
                    # Let's assume non-Apple smartphones are Android for this dataset
                    match = True 
                elif req_tag in p_tags:
                    match = True
            
            if match:
                filtered_products.append(p)
                
        if filtered_products:
            products = filtered_products

    # Search in specs (deep search)
    # If no results from basic filters, or if we want to refine
    if not products and not filters: # Only if nothing specific was found
         pass # Handled by fuzzy search below
    
    # Enhanced Fuzzy search logic
    scored_products = []
    # If we have some initial filtering, score those
    target_products = products if products else Product.query.all()
    
    for p in target_products:
        # Match against name, tags, description AND SPECS for better recall
        # We include specs values in search content
        specs_str = ""
        if p.specs:
             specs_str = " ".join(re.findall(r'"[^"]*"\s*:\s*"([^"]*)"', p.specs)) # Extract values from JSON string
             
        search_content = f"{p.name} {p.tags} {p.category} {p.description} {specs_str}"
        score = fuzz.partial_ratio(lower_msg, search_content.lower())
        
        # Boost score if category matches explicitly
        if 'category' in filters and p.category == filters['category']:
            score += 20
        
        # Boost if Android requested and not Apple (already filtered but good for scoring)
        if 'android' in filters.get('tags', []) and 'apple' not in p.tags:
            score += 15

        scored_products.append((score, p))
            
    scored_products.sort(key=lambda x: x[0], reverse=True)
    
    # Threshold for relevance
    # If we have specific filters (like 'android'), we might want to be more lenient with score
    # or rely on the filter results if fuzzy search fails?
    
    # If we have strong filters (category/tags), trust them more
    if filters:
        final_products = products
        # If too many, sort by score
        if len(final_products) > 5:
             # re-score just these
             final_products_scored = []
             for p in final_products:
                 # simple score
                 specs_str = ""
                 if p.specs:
                      specs_str = " ".join(re.findall(r'"[^"]*"\s*:\s*"([^"]*)"', p.specs))
                 search_content = f"{p.name} {p.tags} {p.category} {specs_str}"
                 s = fuzz.partial_ratio(lower_msg, search_content.lower())
                 final_products_scored.append((s, p))
             final_products_scored.sort(key=lambda x: x[0], reverse=True)
             final_products = [p for s, p in final_products_scored][:10] # Show more for broad queries
    else:
        final_products = [p for s, p in scored_products if s > 45][:5]
    
    # If no filters were extracted AND fuzzy search yielded low results, show random popular
    if not final_products:
        reply_text = "Я не совсем понял запрос, но вот популярные товары, которые могут вам понравиться:"
        final_products = Product.query.order_by(Product.price.desc()).limit(3).all()
    else:
        reply_text = f"Нашел {len(final_products)} вариантов для вас:"

    result_products = [p.to_dict() for p in final_products]
    
    return jsonify({
        'reply': reply_text,
        'products': result_products
    })

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.limit(20).all()
    return jsonify([p.to_dict() for p in products])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
