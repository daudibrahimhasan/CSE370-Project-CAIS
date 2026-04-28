import os
import django
from django.db import connection, transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cais_project.settings")
django.setup()


def seed_court_data(cursor):
    cursor.execute(
        """
        UPDATE court_court
        SET
            verdict = CASE
                WHEN MOD(court_id, 5) = 0 THEN 'PENDING'
                WHEN MOD(court_id, 5) = 1 THEN 'GUILTY'
                WHEN MOD(court_id, 5) = 2 THEN 'NOT_GUILTY'
                WHEN MOD(court_id, 5) = 3 THEN 'DISMISSED'
                ELSE 'PLEA_DEAL'
            END,
            verdict_date = CASE
                WHEN MOD(court_id, 5) = 0 THEN NULL
                ELSE DATE_ADD(TIMESTAMP(court_date), INTERVAL MOD(court_id, 8) DAY)
            END,
            sentence_type = CASE
                WHEN MOD(court_id, 5) = 1 THEN 'PRISON'
                WHEN MOD(court_id, 5) = 2 THEN 'NONE'
                WHEN MOD(court_id, 5) = 3 THEN 'NONE'
                WHEN MOD(court_id, 5) = 4 THEN 'PROBATION'
                ELSE NULL
            END,
            sentence_length_months = CASE
                WHEN MOD(court_id, 5) = 1 THEN 12 + MOD(court_id, 48)
                WHEN MOD(court_id, 5) = 4 THEN 6 + MOD(court_id, 18)
                ELSE NULL
            END,
            fine_amount = CASE
                WHEN MOD(court_id, 5) = 4 THEN 5000 + (MOD(court_id, 12) * 750)
                ELSE NULL
            END,
            verdict_notes = CASE
                WHEN MOD(court_id, 5) = 0 THEN 'Hearing adjourned pending final evidence review.'
                WHEN MOD(court_id, 5) = 1 THEN 'Conviction entered after witness corroboration and forensic confirmation.'
                WHEN MOD(court_id, 5) = 2 THEN 'Acquittal entered due to insufficient direct evidence.'
                WHEN MOD(court_id, 5) = 3 THEN 'Case dismissed following procedural defect in filing.'
                ELSE 'Plea agreement approved with supervised release conditions.'
            END
        """
    )
    return cursor.rowcount


def seed_criminal_data(cursor):
    sectors = [
        "Amazon Lily",
        "Impel Down",
        "Marineford",
        "Fish-Man Island",
        "Punk Hazard",
        "Dressrosa",
        "Zou",
        "Whole Cake Island",
        "Wano Country",
        "Egghead",
        "Elbaf",
    ]
    sector_cases = " ".join(
        [f"WHEN {index} THEN '{sector}'" for index, sector in enumerate(sectors)]
    )

    cursor.execute(
        f"""
        UPDATE criminals_criminal
        SET
            sector_name = CASE MOD(criminal_id - 1, {len(sectors)})
                {sector_cases}
            END,
            current_status = CASE
                WHEN MOD(criminal_id, 5) IN (1, 2) THEN 'IN_JAIL'
                WHEN MOD(criminal_id, 5) = 3 THEN 'WANTED'
                WHEN MOD(criminal_id, 5) = 4 THEN 'RELEASED'
                ELSE 'UNKNOWN'
            END,
            jail_name = CASE
                WHEN MOD(criminal_id, 5) IN (1, 2) THEN
                    CASE
                        WHEN MOD(criminal_id, 4) = 0 THEN 'Impel Down'
                        WHEN MOD(criminal_id, 4) = 1 THEN 'Marineford Holding'
                        WHEN MOD(criminal_id, 4) = 2 THEN 'Wano Detention Block'
                        ELSE 'Egghead Security Wing'
                    END
                ELSE NULL
            END,
            jail_number = CASE
                WHEN MOD(criminal_id, 5) IN (1, 2) THEN CONCAT('J-', LPAD(criminal_id, 4, '0'))
                ELSE NULL
            END,
            status_updated_at = NOW()
        """
    )
    return cursor.rowcount


def seed_assignment_data(cursor):
    cursor.execute("SELECT COUNT(*) FROM officers_assignment")
    existing = cursor.fetchone()[0]
    if existing:
        return 0

    cursor.execute(
        """
        INSERT INTO officers_assignment (
            task_type,
            status,
            priority,
            assigned_at,
            due_at,
            completed_at,
            notes,
            officer_id,
            crime_id,
            criminal_id,
            case_id,
            warrant_id
        )
        SELECT
            CASE
                WHEN MOD(o.officer_id, 5) = 0 THEN 'INVESTIGATE_CRIME'
                WHEN MOD(o.officer_id, 5) = 1 THEN 'SURVEILLANCE_CRIMINAL'
                WHEN MOD(o.officer_id, 5) = 2 THEN 'ARREST'
                WHEN MOD(o.officer_id, 5) = 3 THEN 'COURT_APPEARANCE'
                ELSE 'EVIDENCE_HANDLING'
            END,
            CASE
                WHEN MOD(o.officer_id, 4) = 0 THEN 'COMPLETED'
                WHEN MOD(o.officer_id, 4) = 1 THEN 'ASSIGNED'
                WHEN MOD(o.officer_id, 4) = 2 THEN 'IN_PROGRESS'
                ELSE 'ASSIGNED'
            END,
            1 + MOD(o.officer_id, 5),
            NOW(),
            DATE_ADD(NOW(), INTERVAL 3 + MOD(o.officer_id, 10) DAY),
            CASE
                WHEN MOD(o.officer_id, 4) = 0 THEN DATE_ADD(NOW(), INTERVAL -1 DAY)
                ELSE NULL
            END,
            CASE
                WHEN MOD(o.officer_id, 5) = 0 THEN 'Lead investigator assigned to collect statements and verify the scene timeline.'
                WHEN MOD(o.officer_id, 5) = 1 THEN 'Maintain surveillance and report all confirmed movements of the subject.'
                WHEN MOD(o.officer_id, 5) = 2 THEN 'Execute apprehension tasking when warrant conditions are met.'
                WHEN MOD(o.officer_id, 5) = 3 THEN 'Prepare case brief and attend the scheduled hearing.'
                ELSE 'Secure evidence chain and submit inventory verification.'
            END,
            o.officer_id,
            CASE
                WHEN MOD(o.officer_id, 5) = 0 THEN 1 + MOD(o.officer_id - 1, 197)
                ELSE NULL
            END,
            CASE
                WHEN MOD(o.officer_id, 5) IN (1, 2) THEN 1 + MOD((o.officer_id * 3) - 1, 200)
                ELSE NULL
            END,
            CASE
                WHEN MOD(o.officer_id, 5) = 3 THEN 1 + MOD(o.officer_id - 1, 180)
                ELSE NULL
            END,
            CASE
                WHEN MOD(o.officer_id, 5) = 2 THEN 1 + MOD(o.officer_id - 1, 105)
                ELSE NULL
            END
        FROM officers_officer o
        """
    )
    return cursor.rowcount


def main():
    with transaction.atomic():
        with connection.cursor() as cursor:
            court_rows = seed_court_data(cursor)
            criminal_rows = seed_criminal_data(cursor)
            assignment_rows = seed_assignment_data(cursor)

    print(f"Updated court rows: {court_rows}")
    print(f"Updated criminal rows: {criminal_rows}")
    print(f"Inserted officer assignments: {assignment_rows}")


if __name__ == "__main__":
    main()
