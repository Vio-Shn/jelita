-- Add shipping_method column to order table if not exists
ALTER TABLE "order" ADD COLUMN shipping_method VARCHAR(50);
