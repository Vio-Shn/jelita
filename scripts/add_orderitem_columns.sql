-- Add product_name and image_url columns to OrderItem table
ALTER TABLE order_item ADD COLUMN product_name VARCHAR(200);
ALTER TABLE order_item ADD COLUMN image_url VARCHAR(500);
