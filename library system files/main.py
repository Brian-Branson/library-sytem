#!/usr/bin/env python3
"""
Library Management System - Main Application
This is the entry point for the library management system.
"""

import sys
import os
from tkinter import messagebox

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function to start the library management system"""

    print("=" * 50)
    print("📚 Library Management System")
    print("=" * 50)

    # Choose between database and in-memory storage
    while True:
        choice = input("\nChoose storage method:\n1. Database (MySQL)\n2. In-Memory (for testing)\nEnter choice (1 or 2): ").strip()

        if choice == "1":
            use_database = True
            break
        elif choice == "2":
            use_database = False
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    system = None
    db = None

    if use_database:
        print("\n🔌 Setting up database connection...")
        try:
            from database_manager import DatabaseManager

            # Get database credentials
            print("\nDatabase Configuration:")
            host = input("MySQL Host (default: localhost): ").strip() or "localhost"
            database = input("Database Name (default: libralog): ").strip() or "libralog"
            user = input("MySQL User (default: root): ").strip() or "root"
            password = input("MySQL Password (press Enter for no password): ").strip()

            # Create database manager
            db = DatabaseManager(host=host, database=database, user=user, password=password)

            # Optional: insert initial data
            insert = input("Insert sample data? (y/n): ").strip().lower()
            if insert == "y":
                db.insert_sample_data()

        except Exception as e:
            print(f"❌ Failed to connect to database: {e}")
            return
    else:
        from library_system import LibrarySystem
        system = LibrarySystem()
        print("✅ In-memory library system initialized.")

    # Launch GUI
    try:
        from gui_application import LibraryGUI
        gui = LibraryGUI(system=system, db=db)
        gui.run()
    except Exception as gui_err:
        print(f"❌ Failed to start GUI: {gui_err}")

if __name__ == "__main__":
    main()
