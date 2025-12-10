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
- Python 3.10+
- pip (Python Package Manager)

## Usage

### Register & Login
1. Buka `https://shnvi.pythonanywhere.com`
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
2. Pilih metode pembayaran
3. Selesaikan pembayaran
4. Order status akan update otomatis

### Track Order
1. Klik "Pesanan Saya" di navigation
2. Klik order untuk melihat detail
3. Lihat status pengiriman dan tracking number

## Support

Untuk bantuan atau pertanyaan, silakan buat issue di GitHub atau hubungi tim support.

## License

© 2025 Jelita E-Commerce. All rights reserved.
