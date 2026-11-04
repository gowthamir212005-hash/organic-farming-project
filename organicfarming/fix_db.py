#!/usr/bin/env python3
"""
Direct SQLite migration to add SMS status columns to farming_order table.
"""
import sqlite3
import sys

db_path = r'c:\Users\Gowthami R\Desktop\final project\organicfarming\db.sqlite3'

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check current schema
    cursor.execute("PRAGMA table_info(farming_order)")
    columns = {row[1]: row for row in cursor.fetchall()}
    
    if 'sms_status' in columns:
        print("✓ sms_status column already exists")
    else:
        print("Adding sms_status column...")
        cursor.execute("""
            ALTER TABLE farming_order 
            ADD COLUMN sms_status VARCHAR(10) DEFAULT 'pending'
        """)
        print("✓ Added sms_status column")
    
    if 'sms_error' in columns:
        print("✓ sms_error column already exists")
    else:
        print("Adding sms_error column...")
        cursor.execute("""
            ALTER TABLE farming_order 
            ADD COLUMN sms_error TEXT DEFAULT ''
        """)
        print("✓ Added sms_error column")
    
    conn.commit()
    print("\n✓ Database schema updated successfully!")
    
    # Verify
    cursor.execute("PRAGMA table_info(farming_order)")
    cols = [row[1] for row in cursor.fetchall()]
    print(f"Order table columns: {cols}")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
finally:
    if conn:
        conn.close()
