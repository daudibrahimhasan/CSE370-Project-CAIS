import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cais_project.settings')
django.setup()

def clear_database():
    with connection.cursor() as cursor:
        print("Disabling foreign key checks...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        
        # Get all tables
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"Found {len(tables)} tables. Clearing data...")
        for table in tables:
            # We want to keep the Django migrations table and maybe admin user?
            # But the user said "clear full database and tables".
            # Truncating is better than dropping if they want to keep the structure.
            try:
                print(f"Truncating {table}...")
                cursor.execute(f"TRUNCATE TABLE `{table}`;")
            except Exception as e:
                print(f"Could not truncate {table}: {e}")
        
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        print("Database cleared.")

if __name__ == "__main__":
    clear_database()
