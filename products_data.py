# products_data.py
# Data dummy produk untuk ditampilkan di website

PRODUCTS = [
    # Paris
    {
        'id': 1,
        'name': 'Paris',
        'category': 'Paris',
        'price': 45000,
        'discount_price': None,
        'description': 'Hijab paris premium dengan bahan berkualitas tinggi',
        'stock': 50,
        'image_url': '/static/images/paris2.webp',
        'images': {
            'Dusty Pink': ['/static/images/paris2.webp', '/static/images/paris2.webp'],
            'Sage Green': ['/static/images/paris1.webp', '/static/images/paris1.webp'],
            'Coklat Muda': ['/static/images/743.webp', '/static/images/743.webp'],
            'Baby Blue': ['/static/images/534.webp', '/static/images/534.webp']
        }
    },
    {
        'id': 2,
        'name': 'Paris',
        'category': 'Paris',
        'price': 45000,
        'discount_price': None,
        'description': 'Hijab paris dengan motif bunga cantik',
        'stock': 30,
        'image_url': '/static/images/hijab2.webp',
        'images': {
            'Coklat Muda': ['/static/images/hijab2.webp', '/static/images/hijab2.webp'],
            'Sage Green': ['/static/images/hijab.webp', '/static/images/hijab.webp'],
            'Dusty Pink': ['/static/images/paris2.webp', '/static/images/paris2.webp'],
            'Dark Green': ['/static/images/paris3.webp', '/static/images/paris3.webp']
        }
    },
    {
        'id': 3,
        'name': 'Paris',
        'category': 'Paris',
        'price': 45000,
        'discount_price': None,
        'description': 'Hijab paris warna pastel lembut',
        'stock': 40,
        'image_url': '/static/images/paris3.webp',
        'images': {
            'Dark Green': ['/static/images/paris3.webp', '/static/images/paris3.webp'],
            'Coklat Muda': ['/static/images/hijab2.webp', '/static/images/hijab2.webp'],
            'Sage Green': ['/static/images/hijab.webp', '/static/images/hijab.webp'],
            'Dusty Pink': ['/static/images/paris2.webp', '/static/images/paris2.webp']
        }
    },
    {
        'id': 4,
        'name': 'Paris',
        'category': 'Paris',
        'price': 45000,
        'discount_price': None,
        'description': 'Hijab paris dengan pola elegan',
        'stock': 35,
        'image_url': '/static/images/534.webp',
        'images': {
            'Baby Blue': ['/static/images/534.webp', '/static/images/534.webp'],
            'Dusty Pink': ['/static/images/paris2.webp', '/static/images/paris2.webp'],
            'Sage Green': ['/static/images/paris1.webp', '/static/images/paris1.webp'],
            'Coklat Muda': ['/static/images/743.webp', '/static/images/743.webp'],
        }
    },

    # Pasmina
    {
        'id': 5,
        'name': 'Rayon',
        'category': 'Pasmina',
        'price': 50000,
        'discount_price': None,
        'description': 'Pasmina dengan bahan lembut dan nyaman',
        'stock': 45,
        'image_url': '/static/images/pashmina2.webp',
        'images': {
            'Sage Green': ['/static/images/pashmina2.webp', '/static/images/pashmina2.webp'],
            'Khaki': ['/static/images/pasmina rayon khaki.webp', '/static/images/pasmina rayon khaki.webp'],
            'Coklat Muda': ['/static/images/pasmina rayon chocolate.webp', '/static/images/pasmina rayon chocolate.webp'],
            'Navy Blue': ['/static/images/pasmina rayon navy.webp', '/static/images/pasmina rayon navy.webp']
        }
    },
    {
        'id': 6,
        'name': 'Rayon',
        'category': 'Pasmina',
        'price': 45000,
        'discount_price': None,
        'description': 'Pasmina ceruti premium',
        'stock': 25,
        'image_url': '/static/images/pasmina rayon dark grey.webp',
        'images': {
            'Dark Grey': ['/static/images/pasmina rayon dark grey.webp', '/static/images/pasmina rayon dark grey.webp'],
            'Sage Green': ['/static/images/pashmina2.webp', '/static/images/pashmina2.webp'],
            'Wood': ['/static/images/pasmina rayon wood.webp', '/static/images/pasmina rayon wood.webp'],
            'Navy Blue': ['/static/images/pasmina rayon navy.webp', '/static/images/pasmina rayon navy.webp']
        }
    },
    {
        'id': 7,
        'name': 'Rayon',
        'category': 'Pasmina',
        'price': 45000,
        'discount_price': None,
        'description': 'Pasmina diamond italiano',
        'stock': 38,
        'image_url': '/static/images/pasmina rayon navy.webp',
        'images': {
            'Navy Blue': ['/static/images/pasmina rayon navy.webp', '/static/images/pasmina rayon navy.webp'],
            'Khaki': ['/static/images/pasmina rayon khaki.webp', '/static/images/pasmina rayon khaki.webp'],
            'Dark Grey': ['/static/images/pasmina rayon dark grey.webp', '/static/images/pasmina rayon dark grey.webp'],
            'Wood': ['/static/images/pasmina rayon wood.webp', '/static/images/pasmina rayon wood.webp']
        }
    },
    {
        'id': 8,
        'name': 'Silk',
        'category': 'Pasmina',
        'price': 55000,
        'discount_price': None,
        'description': 'Pasmina rawis premium',
        'stock': 42,
        'image_url': '/static/images/pasmina_dusty.jpg',
        'images': {
            'Dusty Pink': ['/static/images/pasmina_dusty.jpg', '/static/images/pasmina_dusty.jpg'],
            'Sage Green': ['/static/images/pasmina_sage.jpg', '/static/images/pasmina_sage.webp'],
            'Ivory': ['/static/images/pasmina_ivory.jpg', '/static/images/pasmina_ivory.jpg'],
            'Maroon': ['/static/images/pasmina_maroon.jpg', '/static/images/pasmina_maroon.jpg']
        }
    },

    # Instan
    {
        'id': 9,
        'name': 'Hijab',
        'category': 'Instan',
        'price': 65000,
        'discount_price': None,
        'description': 'Hijab instan bergo praktis',
        'stock': 55,
        'image_url': '/static/images/instant_dustypink.jpg',
        'images': {
            'Dusty Pink': ['/static/images/instant_dustypink.jpg', '/static/images/instant_dustypink.jpg'],
            'Clear White': ['/static/images/instant_white.jpg', '/static/images/instant_white.jpg'],
            'Cream': ['/static/images/instant_cream.jpg', '/static/images/instant_cream.jpg'],
            'Baby Blue': ['/static/images/instant_babyblue.jpg', '/static/images/instant_babyblue.jpg']
        }
    },
    {
        'id': 10,
        'name': 'Hijab',
        'category': 'Instan',
        'price': 65000,
        'discount_price': None,
        'description': 'Hijab instan khimar syari',
        'stock': 20,
        'image_url': '/static/images/instant_taupe.jpg',
        'images': {
            'Taupe': ['/static/images/instant_taupe.jpg', '/static/images/instant_taupe.jpg'],
            'Cream': ['/static/images/instant_cream.jpg', '/static/images/instant_cream.jpg'],
            'Baby Blue': ['/static/images/instant_babyblue.jpg', '/static/images/instant_babyblue.jpg'],
            'Dusty Pink': ['/static/images/instant_dustypink.jpg', '/static/images/instant_dustypink.jpg']
        }
    },
    {
        'id': 11,
        'name': 'Syari',
        'category': 'Instan',
        'price': 95000,
        'discount_price': None,
        'description': 'Hijab instan pet antem',
        'stock': 33,
        'image_url': '/static/images/bbypink.jpg',
        'images': {
            'Dusty Pink': ['/static/images/bbypink.jpg', '/static/images/bbypink.webp'],
            'Cream': ['/static/images/cream.jpg', '/static/images/cream.webp'],
            'Coklat Muda': ['/static/images/coklat.jpg', '/static/images/coklat.webp'],
            'Baby Blue': ['/static/images/bbyblue.jpg', '/static/images/bbyblue.webp']
        }
    },
    {
        'id': 12,
        'name': 'Hijab',
        'category': 'Instan',
        'price': 95000,
        'discount_price': None,
        'description': 'Hijab instan syari',
        'stock': 28,
        'image_url': '/static/images/taupe.jpg',
        'images': {
            'Taupe': ['/static/images/taupe.webp', '/static/images/taupe.webp'],
            'Baby Blue': ['/static/images/bbyblue.jpg', '/static/images/bbyblue.webp'],
            'Dusty Pink': ['/static/images/bbypink.jpg', '/static/images/bbypink.webp'],
            'Coklat Muda': ['/static/images/coklat.jpg', '/static/images/coklat.webp']
        }
    },

    # Segi Empat
    {
        'id': 13,
        'name': 'Hijab',
        'category': 'Segi Empat',
        'price': 45000,
        'discount_price': None,
        'description': 'Kerudung segi empat voal',
        'stock': 60,
        'image_url': '/static/images/segiempat coral.webp',
        'images': {
            'Coral': ['/static/images/segiempat coral.webp', '/static/images/segiempat coral.webp'],
            'Floral': ['/static/images/segiempat petite floral.webp', '/static/images/segiempat petite floral.webp'],
            'Garden Veil': ['/static/images/segiempat garden veil.webp', '/static/images/segiempat garden veil.webp'],
            'Regal Lace': ['/static/images/segiempat regal lace.webp', '/static/images/segiempat regal lace.webp']
        }
    },
    {
        'id': 14,
        'name': 'Hijab',
        'category': 'Segi Empat',
        'price': 45000,
        'discount_price': None,
        'description': 'Kerudung segi empat maxmara',
        'stock': 48,
        'image_url': '/static/images/segiempat petite floral.webp',
        'images': {
            'Floral': ['/static/images/segiempat petite floral.webp', '/static/images/segiempat petite floral.webp'],
            'Coral': ['/static/images/segiempat coral.webp', '/static/images/segiempat coral.webp'],
            'Garden Veil': ['/static/images/segiempat garden veil.webp', '/static/images/segiempat garden veil.webp'],
            'Regal Lace': ['/static/images/segiempat regal lace.webp', '/static/images/segiempat regal lace.webp']
        }
    },

    # Aksesoris
    {
        'id': 15,
        'name': 'Bros',
        'category': 'Aksesoris',
        'price': 35000,
        'discount_price': None,
        'description': 'Bros mutiara premium',
        'stock': 100,
        'image_url': '/static/images/aksesoris.webp',
        'images': {
            'Set': ['/static/images/aksesoris.webp', '/static/images/aksesoris.webp']}
    },
    {
        'id': 16,
        'name': 'Tuspin',
        'category': 'Aksesoris',
        'price': 15000,
        'discount_price': None,
        'description': 'Tuspin jilbab & hijab motif',
        'stock': 80,
        'image_url': '/static/images/tuspin.webp',
        'images': {
            'Set': ['/static/images/tuspin.webp', '/static/images/tuspin.webp']
        }
    },
]

CATEGORIES = ['Paris', 'Pasmina', 'Instan', 'Segi Empat', 'Aksesoris']


def get_all_products():
    """Ambil semua produk"""
    return PRODUCTS


def get_products_by_category(category):
    """Filter produk berdasarkan kategori"""
    return [p for p in PRODUCTS if p['category'] == category]


def get_product_by_id(product_id):
    """Ambil produk berdasarkan ID"""
    return next((p for p in PRODUCTS if p['id'] == product_id), None)


def get_categories():
    """Ambil semua kategori"""
    return CATEGORIES
