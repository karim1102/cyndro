#!/usr/bin/env python3
"""
Script to verify the pilot_program.db database is working correctly
"""
import sqlite3
import os

def check_database():
    db_path = "./pilot_program.db"
    
    print("=" * 60)
    print("DATABASE VERIFICATION REPORT")
    print("=" * 60)
    
    # Check if database file exists
    if os.path.exists(db_path):
        print(f"✅ Database file exists: {db_path}")
        print(f"   File size: {os.path.getsize(db_path)} bytes")
    else:
        print(f"❌ Database file NOT found: {db_path}")
        print("   → Run the FastAPI server first to create the database")
        return
    
    print()
    
    # Connect and check structure
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='pilot_signups'
        """)
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ Table 'pilot_signups' exists")
        else:
            print("❌ Table 'pilot_signups' NOT found")
            conn.close()
            return
        
        # Get table schema
        cursor.execute("PRAGMA table_info(pilot_signups)")
        columns = cursor.fetchall()
        
        print("\n📋 Table Schema:")
        print("-" * 60)
        for col in columns:
            col_id, name, col_type, not_null, default, pk = col
            print(f"   {name:15} | {col_type:10} | PK: {bool(pk)} | NOT NULL: {bool(not_null)}")
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM pilot_signups")
        count = cursor.fetchone()[0]
        
        print(f"\n📊 Total Signups: {count}")
        
        # Show recent signups if any exist
        if count > 0:
            cursor.execute("""
                SELECT id, name, email, created_at 
                FROM pilot_signups 
                ORDER BY created_at DESC 
                LIMIT 5
            """)
            records = cursor.fetchall()
            
            print("\n📝 Recent Signups (last 5):")
            print("-" * 60)
            for rec in records:
                rec_id, name, email, created_at = rec
                print(f"   ID: {rec_id} | {name} | {email}")
                print(f"           Created: {created_at}")
        else:
            print("\n💡 No signups yet. Database is ready to receive data!")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ DATABASE IS WORKING CORRECTLY")
        print("=" * 60)
        
    except sqlite3.Error as e:
        print(f"\n❌ Database error: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    check_database()