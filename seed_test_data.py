import datetime
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cais_project.settings')
django.setup()

from django.db import connection


def seed():
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO officers_team (team_name) VALUES (%s)", ["Narcotics"])
        narcotics_id = cursor.lastrowid
        cursor.execute("INSERT INTO officers_team (team_name) VALUES (%s)", ["Traffic"])
        traffic_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO officers_officer (name, rank, badge_number, team_id)
            VALUES (%s, %s, %s, %s)
            """,
            ["James Bond", "Detective", "007", narcotics_id],
        )
        officer_one_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO officers_officer (name, rank, badge_number, team_id)
            VALUES (%s, %s, %s, %s)
            """,
            ["Sarah Connor", "Sergeant", "SC101", traffic_id],
        )
        officer_two_id = cursor.lastrowid

        today = datetime.date.today()
        cursor.execute(
            """
            INSERT INTO officers_shift (officer_id, date, hours_worked)
            VALUES (%s, %s, %s), (%s, %s, %s)
            """,
            [officer_one_id, today, 8, officer_two_id, today, 10],
        )

        cursor.execute(
            """
            INSERT INTO criminals_criminal (name, age, date_of_birth, gender, physical_description, is_repeat_offender)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            ["John Doe", 30, datetime.date(1994, 1, 1), "Male", "Scar on left eye, snake tattoo on arm", False],
        )
        criminal_one_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO criminals_criminal (name, age, date_of_birth, gender, physical_description, is_repeat_offender)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            ["Jane Smith", 25, datetime.date(1999, 5, 20), "Female", "Height 5'6, blonde hair", False],
        )
        criminal_two_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO criminals_nickname (criminal_id, alias)
            VALUES (%s, %s), (%s, %s)
            """,
            [criminal_one_id, "The Snake", criminal_one_id, "Johnny"],
        )
        cursor.execute(
            """
            INSERT INTO criminals_interrogation (officer_id, criminal_id, date, notes)
            VALUES (%s, %s, %s, %s)
            """,
            [officer_one_id, criminal_one_id, datetime.datetime.now(), "Subject refused to speak without lawyer."],
        )

        crime_method = "Smashed front window with a brick"
        now = datetime.datetime.now()
        crime_rows = [
            ("Jewelry store heist", crime_method, "Downtown", now, "Open"),
            ("Clothing store robbery", crime_method, "Uptown", now - datetime.timedelta(days=2), "Open"),
            ("Random assault", "Physical fight", "Park", now - datetime.timedelta(days=5), "Closed"),
        ]
        crime_ids = []
        for description, method_used, location, date_time, status in crime_rows:
            cursor.execute(
                """
                INSERT INTO crimes_crime (description, method_used, location, date_time, status, city, latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, NULL, NULL, NULL)
                """,
                [description, method_used, location, date_time, status],
            )
            crime_ids.append(cursor.lastrowid)

        cursor.execute(
            """
            INSERT INTO crimes_crimeinvolvement (criminal_id, crime_id)
            VALUES (%s, %s), (%s, %s), (%s, %s)
            """,
            [criminal_one_id, crime_ids[0], criminal_one_id, crime_ids[1], criminal_two_id, crime_ids[2]],
        )

        cursor.execute("INSERT INTO crimes_victim (name) VALUES (%s)", ["Alice Wonderland"])
        victim_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO crimes_victimphone (victim_id, phone_number) VALUES (%s, %s)",
            [victim_id, "01812345678"],
        )
        cursor.execute(
            "INSERT INTO crimes_crimevictim (crime_id, victim_id) VALUES (%s, %s)",
            [crime_ids[0], victim_id],
        )
        cursor.execute(
            """
            INSERT INTO crimes_evidence (crime_id, type, description)
            VALUES (%s, %s, %s), (%s, %s, %s)
            """,
            [
                crime_ids[0], "Brick", "Red clay brick found inside the store.",
                crime_ids[1], "Brick", "Broken brick fragments.",
            ],
        )
        cursor.execute(
            """
            INSERT INTO warrants_warrant (criminal_id, issue_date, status)
            VALUES (%s, %s, %s), (%s, %s, %s)
            """,
            [criminal_one_id, today, "Active", criminal_two_id, today, "Cancelled"],
        )
        cursor.execute(
            """
            INSERT INTO cases_case (crime_id, status, opened_date)
            VALUES (%s, %s, %s)
            """,
            [crime_ids[0], "Open", today],
        )
        case_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO court_court (case_id, court_date, judge_name)
            VALUES (%s, %s, %s)
            """,
            [case_id, today + datetime.timedelta(days=30), "John Marshall"],
        )

    print("Database seeded successfully!")


if __name__ == "__main__":
    seed()
