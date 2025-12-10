# Jelita E-Commerce Platform

Platform e-commerce modern untuk Muslim fashion brand dengan fitur lengkap termasuk user authentication, shopping cart, order tracking, dan payment gateway integration dengan Midtrans.

## Features

- User Authentication (Register, Login, Logout)
- Product Catalog dengan Filter dan Search
- Shopping Cart Management
- Order Checkout dengan Multiple Payment Methods
- Midtrans Payment Gateway Integration
- Order Tracking dan Shipping Details
- User Profile Management
- Responsive Design dengan Tailwind CSS

## Tech Stack

- **Backend**: Flask dengan Python
- **Database**: SQLite
- **Authentication**: Flask-Login
- **Payment Gateway**: Midtrans
- **Frontend**: HTML, CSS (Tailwind), JavaScript
- **ORM**: SQLAlchemy

## Installation

### Prerequisites
- Python 3.8+
- pip (Python Package Manager)

### Steps

1. **Clone atau download project**
\`\`\`bash
cd jelita-ecommerce
\`\`\`

2. **Create Virtual Environment**
\`\`\`bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
\`\`\`

3. **Install Dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. **Setup Environment Variables**
Buat file `.env` di root directory:
\`\`\`
SECRET_KEY=your-secret-key-here
MIDTRANS_SERVER_KEY=your-midtrans-server-key
MIDTRANS_CLIENT_KEY=your-midtrans-client-key
MIDTRANS_ENVIRONMENT=sandbox
\`\`\`

5. **Initialize Database**
\`\`\`bash
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
>>> exit()
\`\`\`

6. **Seed Sample Data**
\`\`\`bash
python seed_products.py
\`\`\`

7. **Run Application**
\`\`\`bash
python app.py
\`\`\`

Aplikasi akan berjalan di `http://localhost:5000`

## Folder Structure

\`\`\`
jelita-ecommerce/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── payment.py             # Midtrans payment integration
├── utils.py               # Helper functions
├── seed_products.py       # Database seeding script
├── requirements.txt       # Python dependencies
├── jelita.db              # SQLite database (created automatically)
├── templates/             # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── products.html
│   ├── product-detail.html
│   ├── cart.html
│   ├── checkout.html
│   ├── orders.html
│   └── order-detail.html
└── static/                # Static files
    ├── css/
    │   └── styles.css
    ├── js/
    │   ├── script.js
    │   └── cart.js
    └── images/            # Product images
\`\`\`

## Usage

### Register & Login
1. Buka `http://localhost:5000`
2. Klik "Register" untuk membuat akun baru
3. Login dengan username dan password

### Browse Products
1. Klik "Produk" di navigation
2. Filter berdasarkan kategori atau harga
3. Klik produk untuk melihat detail

### Add to Cart & Checkout
1. Di halaman detail produk, pilih warna dan ukuran
2. Tentukan quantity
3. Klik "Tambah ke Keranjang"
4. Buka cart untuk review
5. Klik "Lanjut ke Pembayaran"
6. Isi data pengiriman
7. Pilih metode pembayaran
8. Klik checkout

### Payment dengan Midtrans
1. Di halaman order detail, klik "Lanjutkan Pembayaran"
2. Pilih metode pembayaran di Snap.js popup
3. Selesaikan pembayaran
4. Order status akan update otomatis

### Track Order
1. Klik "Pesanan Saya" di navigation
2. Klik order untuk melihat detail
3. Lihat status pengiriman dan tracking number

## Midtrans Setup

1. Daftar di [Midtrans Dashboard](https://dashboard.midtrans.com)
2. Copy SERVER_KEY dan CLIENT_KEY
3. Update di file `.env`
4. Ubah MIDTRANS_ENVIRONMENT ke 'production' jika sudah live

## Database Models

### User
- id, username, email, password_hash
- phone, address, city, postal_code
- created_at

### Product
- id, name, description, price, discount_price
- category, stock, image_url
- colors, sizes (JSON format)
- rating, reviews_count

### CartItem
- id, user_id, product_id
- quantity, color, size
- added_at

### Order
- id, order_number, user_id
- total_amount, tax_amount, shipping_cost, discount_amount
- status, payment_status, payment_method
- shipping_address, tracking_number
- created_at, updated_at

### OrderItem
- id, order_id, product_id
- quantity, price, color, size

## API Endpoints

### Products
- `GET /` - Homepage
- `GET /products` - Product catalog
- `GET /product/<id>` - Product detail

### Authentication
- `POST /register` - Register user
- `POST /login` - Login user
- `GET /logout` - Logout user

### Cart
- `GET /cart` - View cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update/<id>` - Update cart item
- `DELETE /api/cart/remove/<id>` - Remove from cart

### Orders
- `GET /checkout` - Checkout page
- `POST /checkout` - Process checkout
- `GET /orders` - List user orders
- `GET /order/<order_number>` - Order detail

### Payment
- `POST /payment/process/<order_number>` - Create payment transaction
- `GET /payment/verify/<order_number>` - Verify payment
- `POST /payment/webhook` - Midtrans webhook

## Troubleshooting

### Database Error
Hapus file `jelita.db` dan jalankan:
\`\`\`bash
python app.py
\`\`\`

### Payment Not Working
- Periksa MIDTRANS_SERVER_KEY dan CLIENT_KEY di `.env`
- Pastikan MIDTRANS_ENVIRONMENT sudah sesuai (sandbox/production)

### Port Already In Use
Ubah di `app.py`:
\`\`\`python
app.run(debug=True, port=5001)
\`\`\`

## Support

Untuk bantuan atau pertanyaan, silakan buat issue di GitHub atau hubungi tim support.

## License

© 2025 Jelita E-Commerce. All rights reserved.
