import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cais_project.settings')
django.setup()

from django.db import connection

from seed_test_data import seed


def sync():
    print("Starting Final Database Sync...")

    delete_order = [
        'court_court',
        'cases_case',
        'warrants_warrant',
        'criminals_interrogation',
        'crimes_evidence',
        'crimes_crimevictim',
        'crimes_crimeinvolvement',
        'crimes_victimphone',
        'crimes_victim',
        'crimes_crime',
        'criminals_nickname',
        'criminals_criminal',
        'officers_shift',
        'officers_officer',
        'officers_team',
    ]

    with connection.cursor() as cursor:
        for table_name in delete_order:
            cursor.execute(f"DELETE FROM {table_name}")

    seed()

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM criminals_criminal")
        criminal_total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM crimes_crime")
        crime_total = cursor.fetchone()[0]

    print(f"Sync Successful: {criminal_total} Criminals and {crime_total} Crimes synchronized.")


if __name__ == "__main__":
    sync()
