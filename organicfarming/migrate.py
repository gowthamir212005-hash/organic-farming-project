#!/usr/bin/env python
"""
Database migration utility for Organic Farm
Run this script to apply pending migrations.
"""
import os
import sys
import subprocess

# Change to the organicfarming directory
os.chdir(r'c:\Users\Gowthami R\Desktop\final project\organicfarming')

# Run makemigrations
print("Step 1: Creating migration files...")
result = subprocess.run([sys.executable, 'manage.py', 'makemigrations', 'farming'], 
                       capture_output=True, text=True)
print(result.stdout if result.stdout else "(No new migrations needed)")
if result.stderr:
    print("Errors:", result.stderr)

# Run migrate
print("\nStep 2: Applying migrations...")
result = subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                       capture_output=True, text=True)
print(result.stdout if result.stdout else "Migration completed")
if result.stderr:
    print("Errors:", result.stderr)

print("\nDone!")
