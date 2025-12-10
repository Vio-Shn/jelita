from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json
from authlib.integrations.flask_client import OAuth
from payment import MidtransPayment
from products_data import get_all_products, get_products_by_category, get_product_by_id, get_categories, PRODUCTS

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-12345'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour
app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL') or 'sqlite:///jelita.db'
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

def migrate_database():
    """Auto-migrate database to add missing columns"""
    with app.app_context():
        inspector = db.inspect(db.engine)
        
        if 'user' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('user')]
            if 'google_id' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE user ADD COLUMN google_id VARCHAR(200)'))
                    conn.commit()
                print("Added google_id column to user table")
        
        # Check and add shipping_method to order table
        if 'order' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('order')]
            if 'shipping_method' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE "order" ADD COLUMN shipping_method VARCHAR(50)'))
                    conn.commit()
                print("Added shipping_method column to order table")
        
        # Check and add product_name and image_url to order_item table
        if 'order_item' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('order_item')]
            
            if 'product_name' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE order_item ADD COLUMN product_name VARCHAR(200)'))
                    conn.commit()
                print("Added product_name column to order_item table")
            
            if 'image_url' not in columns:
                with db.engine.connect() as conn:
                    conn.execute(db.text('ALTER TABLE order_item ADD COLUMN image_url VARCHAR(500)'))
                    conn.commit()
                print("Added image_url column to order_item table")

@app.template_filter('from_json')
def from_json_filter(value):
    """Parse JSON string to Python object"""
    if not value:
        return []
    try:
        return json.loads(value)
    except:
        return []

# ==================== DATABASE MODELS ====================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=True)  # Nullable for Google OAuth users
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(10))
    google_id = db.Column(db.String(200))  # For Google OAuth
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float)
    category = db.Column(db.String(50), nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    colors = db.Column(db.String(200))  # JSON format: ["Black", "White", "Maroon"]
    sizes = db.Column(db.String(200))   # JSON format: ["S", "M", "L", "XL"]
    rating = db.Column(db.Float, default=0)
    reviews_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    cart_items = db.relationship('CartItem', backref='product', lazy=True, cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def get_final_price(self):
        return self.discount_price if self.discount_price else self.price


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    color = db.Column(db.String(50))
    size = db.Column(db.String(10))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_subtotal(self):
        if self.product is None:
            return 0
        return self.product.get_final_price() * self.quantity


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_number = db.Column(db.String(50), unique=True)
    total_amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0)
    tax_amount = db.Column(db.Float, default=0)
    shipping_cost = db.Column(db.Float, default=0)
    shipping_method = db.Column(db.String(50))
    status = db.Column(db.String(50), default='pending')  # pending, paid, processing, shipped, delivered
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50), default='unpaid')  # unpaid, paid
    payment_id = db.Column(db.String(100))
    shipping_address = db.Column(db.Text)
    shipping_city = db.Column(db.String(100))
    shipping_postal = db.Column(db.String(10))
    tracking_number = db.Column(db.String(50))
    estimated_delivery = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def generate_order_number(self):
        import random
        import string
        self.order_number = 'ORD-' + datetime.utcnow().strftime('%Y%m%d') + '-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(200))
    image_url = db.Column(db.String(500))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    color = db.Column(db.String(50))
    size = db.Column(db.String(10))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== CONTEXT PROCESSOR ====================

@app.context_processor
def inject_cart_count():
    """Make cart count available to all templates"""
    cart_count = 0
    if current_user.is_authenticated:
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        cart_count = sum(item.quantity for item in cart_items)
        print(f"[v0] Context Processor - User {current_user.id}: Found {len(cart_items)} cart items, total quantity: {cart_count}")
        for item in cart_items:
            print(f"[v0]   - Product {item.product_id}: quantity {item.quantity}")
    else:
        session_cart = session.get('cart', [])
        cart_count = sum(item.get('quantity', 1) for item in session_cart)
        print(f"[v0] Context Processor - Session cart: {len(session_cart)} items, total quantity: {cart_count}")
    
    return dict(cart_count=cart_count)

# ==================== ROUTES ====================

@app.route('/')
def index():
    all_products = get_all_products()
    featured_products = all_products[:8]  # Get first 8 products
    return render_template('index.html', featured_products=featured_products)


@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    
    if category:
        all_products = get_products_by_category(category)
    else:
        all_products = get_all_products()
    
    # Manual pagination
    per_page = 12
    total_products = len(all_products)
    total_pages = (total_products + per_page - 1) // per_page  # Ceiling division
    start = (page - 1) * per_page
    end = start + per_page
    products_page = all_products[start:end]
    
    categories = get_categories()
    
    return render_template('products.html', 
                         products=products_page,
                         categories=categories, 
                         selected_category=category,
                         total_pages=total_pages,
                         current_page=page)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = get_product_by_id(product_id)
    
    if not product:
        return "Product not found", 404
    
    # Get related products from same category
    all_products = get_products_by_category(product['category'])
    related_products = [p for p in all_products if p['id'] != product_id][:4]
    
    return render_template('product-detail.html', product=product, related_products=related_products)


@app.route('/cart')
@login_required
def cart():
    print("[v0] Cart page accessed")
    print(f"[v0] User authenticated: {current_user.is_authenticated}")
    
    cart_items_db = CartItem.query.filter_by(user_id=current_user.id).all()
    print(f"[v0] Found {len(cart_items_db)} cart items in database")
    
    cart_items_display = []
    for item in cart_items_db:
        product = get_product_by_id(item.product_id)
        if product:
            display_item = {
                'id': item.id,
                'product_id': item.product_id,
                'name': product['name'],
                'image': product['image_url'],
                'color': item.color,
                'size': item.size,
                'price': product.get('discount_price') or product['price'],
                'quantity': item.quantity,
                'subtotal': (product.get('discount_price') or product['price']) * item.quantity
            }
            cart_items_display.append(display_item)
        else:
            # Remove invalid cart items
            db.session.delete(item)
    
    db.session.commit()
    
    subtotal = sum(item['subtotal'] for item in cart_items_display)
    tax = subtotal * 0.1
    total = subtotal + tax

    print(f"[v0] Cart items to display: {len(cart_items_display)}, subtotal: {subtotal}")
    
    return render_template('cart.html', 
                         cart_items=cart_items_display, 
                         subtotal=subtotal, 
                         tax=tax,
                         total=total)


@app.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    print("[v0] === Add to cart called ===")
    product_id = int(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))
    color = request.form.get('color', 'Default')
    size = request.form.get('size', 'M')
    
    print(f"[v0] Product ID from form: {product_id}")
    print(f"[v0] User authenticated: {current_user.is_authenticated}")
    
    product = get_product_by_id(product_id)
    
    if not product:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Produk tidak ditemukan!'}), 404
        flash('Produk tidak ditemukan!', 'error')
        return redirect(request.referrer or url_for('products'))
    
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()
    
    if cart_item:
        # Update existing item
        cart_item.quantity += quantity
        print(f"[v0] Updated existing cart item, new quantity: {cart_item.quantity}")
    else:
        # Create new cart item
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity,
            color=color,
            size=size
        )
        db.session.add(cart_item)
        print(f"[v0] Added new cart item for product {product_id}")
    
    try:
        db.session.commit()
        
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        new_cart_count = sum(item.quantity for item in cart_items)
        print(f"[v0] New cart count after add: {new_cart_count}")
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'success': True,
                'message': f'Produk "{product["name"]}" berhasil ditambahkan ke keranjang!',
                'cart_count': new_cart_count
            })
        
        flash(f'Produk "{product["name"]}" berhasil ditambahkan ke keranjang!', 'success')
        print(f"[v0] Cart item saved to database successfully")
    except Exception as e:
        db.session.rollback()
        print(f"[v0] Error saving cart item: {str(e)}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Terjadi kesalahan saat menambahkan ke keranjang.'}), 500
        
        flash('Terjadi kesalahan saat menambahkan ke keranjang.', 'error')
    
    return redirect(request.referrer or url_for('products'))

@app.route('/api/cart/remove/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        
        cart_count = db.session.query(db.func.sum(CartItem.quantity)).filter_by(user_id=current_user.id).scalar() or 0
        
        return jsonify({'status': 'success', 'cart_count': cart_count})
    return jsonify({'status': 'error', 'message': 'Item tidak ditemukan'})

@app.route('/api/cart/update/<int:item_id>', methods=['PUT'])
@login_required
def update_cart_quantity(item_id):
    data = request.get_json()
    new_quantity = data.get('quantity')
    
    if not new_quantity or new_quantity < 1:
        return jsonify({'status': 'error', 'message': 'Quantity tidak valid'})
    
    cart_item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if cart_item:
        cart_item.quantity = new_quantity
        db.session.commit()
        
        cart_count = db.session.query(db.func.sum(CartItem.quantity)).filter_by(user_id=current_user.id).scalar() or 0
        
        return jsonify({'status': 'success', 'cart_count': cart_count})
    return jsonify({'status': 'error', 'message': 'Item tidak ditemukan'})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        phone = data.get('phone')
        
        if password != password_confirm:
            return render_template('register.html', error='Passwords do not match')
        
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error='Username already exists')
        
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already exists')
        
        user = User(username=username, email=email, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User.query.filter_by(email=username).first()
        
        if not user or not user.check_password(password):
            return render_template('login.html', error='Invalid username/email or password')
        
        login_user(user)
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/login/google/callback')
def google_callback():
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            flash('Failed to get user info from Google', 'error')
            return redirect(url_for('login'))
        
        google_id = user_info.get('sub')
        email = user_info.get('email')
        name = user_info.get('name')
        
        # Check if user exists by google_id
        user = User.query.filter_by(google_id=google_id).first()
        
        if not user:
            # Check if user exists by email
            user = User.query.filter_by(email=email).first()
            
            if user:
                # Link existing account with Google
                user.google_id = google_id
                db.session.commit()
            else:
                # Create new user
                username = email.split('@')[0]
                # Ensure username is unique
                base_username = username
                counter = 1
                while User.query.filter_by(username=username).first():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User(
                    username=username,
                    email=email,
                    google_id=google_id
                )
                db.session.add(user)
                db.session.commit()
        
        login_user(user)
        flash(f'Welcome, {name}!', 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        print(f"[v0] Google OAuth error: {str(e)}")
        flash('Failed to authenticate with Google', 'error')
        return redirect(url_for('login'))

@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)


@app.route('/order/<order_number>')
@login_required
def order_detail(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    
    if order.user_id != current_user.id:
        return redirect(url_for('index'))
    
    from products_data import get_product_by_id
    for item in order.items:
        if not item.image_url:
            product = get_product_by_id(item.product_id)
            if product:
                item.image_url = product.get('image_url', '/placeholder.svg?height=100&width=100')
    
    return render_template('order-detail.html', order=order)


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if request.method == 'POST':
        # This should not be reached anymore, redirect to process_payment
        return redirect(url_for('process_payment'))
    
    # GET request - show checkout form
    selected_item_ids = request.args.getlist('items')
    
    if not selected_item_ids:
        flash('Silakan pilih item untuk checkout', 'warning')
        return redirect(url_for('cart'))
    
    # Convert to integers
    selected_item_ids = [int(id) for id in selected_item_ids]
    
    selected_items_str = ','.join(map(str, selected_item_ids))
    
    # Get cart items from database
    cart_items_db = CartItem.query.filter(
        CartItem.user_id == current_user.id,
        CartItem.id.in_(selected_item_ids)
    ).all()
    
    if not cart_items_db:
        flash('Item yang dipilih tidak valid', 'warning')
        return redirect(url_for('cart'))
    
    cart_items = []
    for item in cart_items_db:
        product = get_product_by_id(item.product_id)
        if not product:
            continue
        
        base_price = product.get('price') or 0
        discount_price = product.get('discount_price')
        final_price = discount_price if discount_price is not None else base_price
        
        item_obj = {
            'id': item.id,
            'product_id': item.product_id,
            'name': product.get('name', ''),
            'image_url': product.get('image_url', ''),
            'quantity': item.quantity or 1,
            'color': item.color,
            'size': item.size,
            'original_price': base_price,
            'discount': discount_price or 0,
            'final_price': final_price,
        }
        cart_items.append(item_obj)
    
    subtotal = sum((item['final_price'] or 0) * (item['quantity'] or 1) for item in cart_items)
    # Calculate discount as 10% of subtotal
    discount = subtotal * 0.1
    shipping = 15000
    total = subtotal - discount + shipping
    
    return render_template('checkout.html', 
                         cart_items=cart_items, 
                         subtotal=subtotal,
                         discount=discount,
                         shipping=shipping,
                         total=total,
                         selected_items=selected_items_str)


@app.route('/process-payment', methods=['POST'])
@login_required
def process_payment():
    selected_items = request.form.get('selected_items', '').split(',')
    selected_items = [item.strip() for item in selected_items if item.strip()]
    
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    payment_method = request.form.get('payment_method')
    shipping_method = request.form.get('shipping_method')
    
    # Get payment-specific details
    bank_choice = request.form.get('bank_choice')
    ewallet_choice = request.form.get('ewallet_choice')
    ewallet_phone = request.form.get('ewallet_phone')
    card_number = request.form.get('card_number')
    card_name = request.form.get('card_name')
    card_expiry = request.form.get('card_expiry')
    card_cvv = request.form.get('card_cvv')
    
    # Get shipping cost based on method
    shipping_costs = {'regular': 15000, 'express': 25000, 'same_day': 50000}
    shipping = shipping_costs.get(shipping_method, 15000)
    
    # Get cart items from database
    selected_item_ids = [int(id) for id in selected_items]
    cart_items_db = CartItem.query.filter(
        CartItem.user_id == current_user.id,
        CartItem.id.in_(selected_item_ids)
    ).all()
    
    if not cart_items_db:
        flash('Item yang dipilih tidak valid', 'error')
        return redirect(url_for('cart'))
    
    # Build order items list
    items_to_order = []
    for item in cart_items_db:
        product = get_product_by_id(item.product_id)
        if product:
            final_price = product.get('discount_price') if product.get('discount_price') else product.get('price', 0)
            print(f"[v0] Product {product['name']} image_url: {product.get('image_url')}")
            items_to_order.append({
                'product_id': item.product_id,
                'name': product['name'],
                'quantity': item.quantity,
                'price': final_price,
                'image_url': product.get('image_url'),
                'color': item.color,
                'size': item.size,
            })
    
    subtotal = sum(item['price'] * item['quantity'] for item in items_to_order)
    tax = subtotal * 0.1
    total = subtotal + tax + shipping
    
    # Generate order number
    import random
    import string
    order_number = 'ORD-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Generate payment instructions based on method
    payment_details = {}
    if payment_method == 'bank_transfer':
        # Generate virtual account number (simulated)
        va_number = ''.join(random.choices(string.digits, k=16))
        bank_names = {
            'bca': 'BCA',
            'mandiri': 'Mandiri',
            'bni': 'BNI',
            'bri': 'BRI'
        }
        payment_details = {
            'type': 'bank_transfer',
            'bank': bank_names.get(bank_choice, 'BCA'),
            'va_number': va_number,
            'account_name': 'PT Jelita Fashion'
        }
    elif payment_method == 'ewallet':
        ewallet_names = {
            'ovo': 'OVO',
            'dana': 'DANA',
            'gopay': 'GoPay'
        }
        payment_details = {
            'type': 'ewallet',
            'provider': ewallet_names.get(ewallet_choice, 'OVO'),
            'phone': ewallet_phone
        }
    elif payment_method == 'credit_card':
        # Mask card number for display
        masked_card = card_number.replace(' ', '')
        masked_card = '**** **** **** ' + masked_card[-4:] if len(masked_card) >= 4 else masked_card
        payment_details = {
            'type': 'credit_card',
            'card_number': masked_card,
            'card_name': card_name
        }
    else:  # COD
        payment_details = {
            'type': 'cod'
        }
    
    import json
    new_order = Order(
        user_id=current_user.id,
        order_number=order_number,
        total_amount=total,
        discount_amount=0,
        tax_amount=tax,
        shipping_cost=shipping,
        shipping_method=shipping_method,
        payment_method=payment_method,
        payment_id=json.dumps(payment_details),
        shipping_address=address,
        shipping_city='',
        shipping_postal='',
        tracking_number='',
        estimated_delivery=datetime.now() + timedelta(days=7),
        status='pending_payment',
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.session.add(new_order)
    db.session.flush()  # Get the order.id
    
    for item_data in items_to_order:
        print(f"[v0] Creating OrderItem with image_url: {item_data.get('image_url', '')}")
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item_data['product_id'],
            product_name=item_data.get('name', ''),
            image_url=item_data.get('image_url', ''),
            quantity=item_data['quantity'],
            price=item_data['price'],
            color=item_data['color'],
            size=item_data['size']
        )
        db.session.add(order_item)
    
    # Commit all changes
    db.session.commit()
    
    print(f"[v0] Order {order_number} created successfully")
    
    # Store order in session for payment confirmation page
    order_data = {
        'order_number': order_number,
        'items': items_to_order,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'total': total,
        'name': name,
        'phone': phone,
        'address': address,
        'payment_method': payment_method,
        'payment_details': payment_details,
        'shipping_method': shipping_method,
        'status': 'pending_payment'
    }
    
    if 'orders' not in session:
        session['orders'] = []
    session['orders'].append(order_data)
    session.modified = True
    
    # Remove checked out items from cart
    for item in cart_items_db:
        db.session.delete(item)
    db.session.commit()
    
    flash('Pesanan berhasil dibuat!', 'success')
    return redirect(url_for('payment_confirmation', order_number=order_number))


@app.route('/payment-confirmation/<order_number>')
@login_required
def payment_confirmation(order_number):
    orders = session.get('orders', [])
    order = None
    
    for o in orders:
        if o['order_number'] == order_number:
            order = o
            break
    
    if not order:
        flash('Pesanan tidak ditemukan', 'error')
        return redirect(url_for('index'))
    
    return render_template('payment-confirmation.html', order=order)


@app.route('/payment/process/<order_number>', methods=['POST'])
@login_required
def process_payment_route(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    
    if order.user_id != current_user.id:
        return redirect(url_for('index'))
    
    payment_result = MidtransPayment.create_transaction(order)
    
    if payment_result['status'] == 'success':
        return jsonify({
            'status': 'success',
            'token': payment_result['token'],
            'client_key': os.environ.get('MIDTRANS_CLIENT_KEY', 'your-client-key-here'),
            'redirect_url': payment_result.get('redirect_url')
        })
    else:
        return jsonify({
            'status': 'error',
            'message': payment_result.get('message', 'Payment processing failed')
        }), 400


@app.route('/payment/verify/<order_number>')
@login_required
def verify_payment_route(order_number):
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    
    if order.user_id != current_user.id:
        return redirect(url_for('index'))
    
    verification = MidtransPayment.verify_payment(order_number)
    
    if verification['status'] == 'success':
        transaction_status = verification['transaction_status']
        
        # Update order status based on payment status
        if transaction_status == 'settlement':
            order.payment_status = 'paid'
            order.status = 'processing'
        elif transaction_status == 'pending':
            order.payment_status = 'unpaid'
            order.status = 'pending'
        elif transaction_status in ['deny', 'expire', 'cancel']:
            order.status = 'cancelled'
        
        db.session.commit()
        return redirect(url_for('order_detail', order_number=order_number))
    else:
        return redirect(url_for('order_detail', order_number=order_number))


@app.route('/payment/webhook', methods=['POST'])
def payment_webhook():
    """Handle Midtrans webhook notifications"""
    notification = request.get_json()
    result = MidtransPayment.handle_notification(notification)
    
    if result['status'] == 'success':
        order_id = result['order_id']
        transaction_status = result['transaction_status']
        
        order = Order.query.filter_by(order_number=order_id).first()
        if order:
            if transaction_status == 'settlement':
                order.payment_status = 'paid'
                order.status = 'processing'
            elif transaction_status in ['deny', 'expire', 'cancel']:
                order.status = 'cancelled'
            
            db.session.commit()
    
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    migrate_database()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
