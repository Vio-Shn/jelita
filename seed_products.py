from app import app, db, Product
import json

def seed_products():
    products = [
        {
            'name': 'Pashmina Elite',
            'description': 'Premium pashmina hijab with luxurious finish. Perfect for everyday wear.',
            'price': 299000,
            'discount_price': 249000,
            'category': 'Pashmina',
            'stock': 50,
            'image_url': '/static/images/pashmina2.webp',
            'colors': json.dumps(['Black', 'White', 'Maroon', 'Beige']),
            'sizes': json.dumps(['One Size']),
            'rating': 4.8,
            'reviews_count': 145
        },
        {
            'name': 'Primrose Scarf',
            'description': 'Beautiful primrose collection with elegant design. Suitable for all occasions.',
            'price': 349000,
            'discount_price': 299000,
            'category': 'Paris',
            'stock': 35,
            'image_url': '/static/images/primrose-1.jpg',
            'colors': json.dumps(['White', 'Cream', 'Mint', 'Pink']),
            'sizes': json.dumps(['One Size']),
            'rating': 4.9,
            'reviews_count': 203
        },
        {
            'name': 'Instant Hijab Comfort',
            'description': 'Comfortable instant hijab with built-in frame. Easy to wear and style.',
            'price': 189000,
            'discount_price': 149000,
            'category': 'Instant',
            'stock': 60,
            'image_url': '/static/images/paris1.webp',
            'colors': json.dumps(['Black', 'Navy', 'Maroon', 'Gray']),
            'sizes': json.dumps(['S', 'M', 'L', 'XL']),
            'rating': 4.7,
            'reviews_count': 289
        },
        {
            'name': 'Paris Premium',
            'description': 'Premium paris hijab with smooth texture. Ideal for formal events.',
            'price': 279000,
            'discount_price': 239000,
            'category': 'Paris',
            'stock': 45,
            'image_url': '/static/images/paris2.webp',
            'colors': json.dumps(['Black', 'White', 'Chocolate', 'Burgundy']),
            'sizes': json.dumps(['One Size']),
            'rating': 4.9,
            'reviews_count': 178
        },
        {
            'name': 'Pashmina Silk',
            'description': 'Silk blend pashmina for ultimate softness and elegance.',
            'price': 349000,
            'discount_price': 299000,
            'category': 'Pashmina',
            'stock': 40,
            'image_url': '/static/images/pashmina-2.jpg',
            'colors': json.dumps(['Blush', 'Sage', 'Lavender', 'Camel']),
            'sizes': json.dumps(['One Size']),
            'rating': 5.0,
            'reviews_count': 98
        },
        {
            'name': 'Hijab Labore Basic',
            'description': 'Basic collection with affordable price. Perfect for everyday use.',
            'price': 99000,
            'discount_price': 79000,
            'category': 'Hijab',
            'stock': 100,
            'image_url': '/static/images/hijab.webp',
            'colors': json.dumps(['Black', 'White', 'Navy', 'Maroon', 'Gray']),
            'sizes': json.dumps(['One Size']),
            'rating': 4.5,
            'reviews_count': 412
        },
        {
            'name': 'Paris Elegant',
            'description': 'Elegant paris design for special occasions.',
            'price': 329000,
            'discount_price': None,
            'category': 'Paris',
            'stock': 30,
            'image_url': '/static/images/paris-2.jpg',
            'colors': json.dumps(['Black', 'White', 'Emerald', 'Rose']),
            'sizes': json.dumps(['One Size']),
            'rating': 4.8,
            'reviews_count': 156
        },
        {
            'name': 'Instant Premium Plus',
            'description': 'Premium instant hijab with enhanced comfort and style.',
            'price': 249000,
            'discount_price': 199000,
            'category': 'Instant',
            'stock': 55,
            'image_url': '/static/images/instant-2.jpg',
            'colors': json.dumps(['Black', 'Navy', 'Olive', 'Plum']),
            'sizes': json.dumps(['M', 'L', 'XL']),
            'rating': 4.9,
            'reviews_count': 267
        },
    ]
    
    with app.app_context():
        # Clear existing products
        Product.query.delete()
        
        # Add new products
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        db.session.commit()
        print(f"Successfully seeded {len(products)} products!")

if __name__ == '__main__':
    seed_products()
