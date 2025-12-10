import sqlite3
import os

# Path to database
db_path = 'jelita.db'

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Check if column exists
    cursor.execute("PRAGMA table_info('order')")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'shipping_method' not in columns:
        print("Adding shipping_method column to order table...")
        cursor.execute('ALTER TABLE "order" ADD COLUMN shipping_method VARCHAR(50)')
        print("✓ shipping_method column added successfully!")
    else:
        print("✓ shipping_method column already exists")
    
    # Commit changes
    conn.commit()
    print("\n✓ Database migration completed successfully!")
    
except Exception as e:
    print(f"✗ Error during migration: {e}")
    conn.rollback()
finally:
    conn.close()
</parameter>
