import os
import django
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cais_project.settings')
django.setup()

def migrate():
    with connection.cursor() as cursor:
        print("Starting data migration from old tables to Django tables...")

        # 1. Teams
        cursor.execute("SELECT TeamID, TeamName FROM team")
        teams = cursor.fetchall()
        for tid, tname in teams:
            cursor.execute("INSERT INTO officers_team (team_id, team_name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE team_name=VALUES(team_name)", [tid, tname])
        print(f"Migrated {len(teams)} teams.")

        # 2. Officers
        cursor.execute("SELECT OfficerID, Name, RankName, BadgeNumber, TeamID FROM officer")
        officers = cursor.fetchall()
        for oid, name, rank, badge, tid in officers:
            cursor.execute("INSERT INTO officers_officer (officer_id, name, rank, badge_number, team_id) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name)", [oid, name, rank, badge, tid])
        print(f"Migrated {len(officers)} officers.")

        # 3. Criminals
        cursor.execute("SELECT CriminalID, Name, Age, DateOfBirth, Gender, PhysicalDescription, IsRepeatOffender FROM criminal")
        criminals = cursor.fetchall()
        for cid, name, age, dob, gender, desc, repeat in criminals:
            cursor.execute("INSERT INTO criminals_criminal (criminal_id, name, age, date_of_birth, gender, physical_description, is_repeat_offender) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name)", [cid, name, age, dob, gender, desc, repeat])
        print(f"Migrated {len(criminals)} criminals.")

        # 4. Crimes
        cursor.execute("SELECT CrimeID, Description, MethodUsed, LocationName, City, Latitude, Longitude, OccurredAt, CrimeStatus FROM crime")
        crimes = cursor.fetchall()
        for cid, desc, method, loc, city, lat, lon, occurred, status in crimes:
            cursor.execute("INSERT INTO crimes_crime (crime_id, description, method_used, location, city, latitude, longitude, date_time, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE description=VALUES(description)", [cid, desc, method, loc, city, lat, lon, occurred, status])
        print(f"Migrated {len(crimes)} crimes.")

        # 5. Victims
        cursor.execute("SELECT VictimID, Name FROM victim")
        victims = cursor.fetchall()
        for vid, name in victims:
            cursor.execute("INSERT INTO crimes_victim (victim_id, name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name=VALUES(name)", [vid, name])
        print(f"Migrated {len(victims)} victims.")

        # 6. Case Records
        cursor.execute("SELECT CaseID, CrimeID, CaseStatus, OpenedDate FROM case_record")
        cases = cursor.fetchall()
        for cid, crime_id, status, opened in cases:
            cursor.execute("INSERT INTO cases_case (case_id, crime_id, status, opened_date) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE status=VALUES(status)", [cid, crime_id, status, opened])
        print(f"Migrated {len(cases)} cases.")

        # 7. Court Dates
        cursor.execute("SELECT CourtID, CaseID, CourtDate, JudgeName FROM court_date")
        courts = cursor.fetchall()
        for cid, case_id, cdate, judge in courts:
            cursor.execute("INSERT INTO court_court (court_id, case_id, court_date, judge_name) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE judge_name=VALUES(judge_name)", [cid, case_id, cdate, judge])
        print(f"Migrated {len(courts)} court dates.")

        # 8. Involvement
        cursor.execute("SELECT CriminalID, CrimeID FROM crime_involvement")
        involvements = cursor.fetchall()
        for criminal_id, crime_id in involvements:
            cursor.execute("INSERT IGNORE INTO crimes_crimeinvolvement (criminal_id, crime_id) VALUES (%s, %s)", [criminal_id, crime_id])
        print(f"Migrated {len(involvements)} involvements.")

        # 9. Warrants
        cursor.execute("SELECT WarrantID, CriminalID, IssueDate, WarrantStatus FROM warrant")
        warrants = cursor.fetchall()
        for wid, criminal_id, issue_date, status in warrants:
            cursor.execute("INSERT INTO warrants_warrant (warrant_id, criminal_id, issue_date, status) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE status=VALUES(status)", [wid, criminal_id, issue_date, status])
        print(f"Migrated {len(warrants)} warrants.")

        print("Migration completed successfully!")

if __name__ == "__main__":
    migrate()
