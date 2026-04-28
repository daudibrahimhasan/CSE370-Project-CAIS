from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render

from connect import dictfetchall, is_logged_in


def shift_tracking(request):
    if not is_logged_in(request):
        return redirect('admin_login')

    if request.method == 'POST':
        form_name = request.POST.get('form_name', '').strip()

        if form_name == 'assign_officer':
            officer_id = request.POST.get('officer_id', '').strip()
            task_type = request.POST.get('task_type', '').strip()
            sector_name = request.POST.get('sector_name', '').strip() or None
            status = request.POST.get('assignment_status', '').strip() or 'ASSIGNED'
            priority = request.POST.get('priority', '').strip() or '3'
            due_at = request.POST.get('due_at', '').strip() or None
            criminal_id = request.POST.get('criminal_id', '').strip() or None
            case_id = request.POST.get('case_id', '').strip() or None
            notes = request.POST.get('notes', '').strip() or None

            if officer_id and task_type:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO officers_assignment (
                            officer_id, task_type, status, priority, sector_name, due_at, criminal_id, case_id, notes, assigned_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                        """,
                        [officer_id, task_type, status, priority, sector_name, due_at, criminal_id, case_id, notes],
                    )
                messages.success(request, "Officer assignment created successfully.")
            else:
                messages.error(request, "Officer and task type are required for assignment.")
        else:
            officer_id = request.POST.get('officer_id', '').strip()
            shift_date = request.POST.get('shift_date', '').strip()
            hours_worked = request.POST.get('hours_worked', '').strip()

            if officer_id and shift_date and hours_worked:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO officers_shift (officer_id, date, hours_worked)
                        VALUES (%s, %s, %s)
                        """,
                        [officer_id, shift_date, hours_worked],
                    )
                messages.success(request, "Shift record added successfully.")
            else:
                messages.error(request, "Officer, shift date, and hours are required.")

        return redirect('shift_tracking')

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

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT officer_id, name, badge_number, rank
            FROM officers_officer
            ORDER BY name
            """
        )
        officers = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT
                s.shift_id,
                s.date,
                s.hours_worked,
                o.officer_id,
                o.name AS officer_name,
                o.rank,
                o.badge_number
            FROM officers_shift s
            JOIN officers_officer o ON s.officer_id = o.officer_id
            ORDER BY s.date DESC, s.shift_id DESC
            """
        )
        shifts = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT criminal_id, name
            FROM criminals_criminal
            ORDER BY name
            """
        )
        criminals = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT case_id, status
            FROM cases_case
            ORDER BY case_id DESC
            """
        )
        cases = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT
                today_shift.officer_id,
                o.name AS officer_name,
                o.rank,
                o.badge_number,
                today_shift.hours_logged,
                active_assignment.task_type,
                active_assignment.status AS assignment_status,
                active_assignment.sector_name,
                active_assignment.priority,
                active_assignment.target_label
            FROM (
                SELECT officer_id, SUM(hours_worked) AS hours_logged
                FROM officers_shift
                WHERE date = CURDATE()
                GROUP BY officer_id
            ) today_shift
            JOIN officers_officer o ON o.officer_id = today_shift.officer_id
            LEFT JOIN (
                SELECT
                    ranked.officer_id,
                    ranked.task_type,
                    ranked.status,
                    ranked.sector_name,
                    ranked.priority,
                    ranked.target_label
                FROM (
                    SELECT
                        oa.officer_id,
                        oa.task_type,
                        oa.status,
                        oa.sector_name,
                        oa.priority,
                        CASE
                            WHEN cc.name IS NOT NULL THEN CONCAT('CRIMINAL: ', cc.name)
                            WHEN cs.case_id IS NOT NULL THEN CONCAT('CASE #', cs.case_id)
                            WHEN cr.crime_id IS NOT NULL THEN CONCAT('CRIME #', cr.crime_id)
                            WHEN ww.warrant_id IS NOT NULL THEN CONCAT('WARRANT #', ww.warrant_id)
                            ELSE 'GENERAL TASKING'
                        END AS target_label,
                        ROW_NUMBER() OVER (
                            PARTITION BY oa.officer_id
                            ORDER BY oa.assigned_at DESC, oa.assignment_id DESC
                        ) AS row_num
                    FROM officers_assignment oa
                    LEFT JOIN criminals_criminal cc ON oa.criminal_id = cc.criminal_id
                    LEFT JOIN cases_case cs ON oa.case_id = cs.case_id
                    LEFT JOIN crimes_crime cr ON oa.crime_id = cr.crime_id
                    LEFT JOIN warrants_warrant ww ON oa.warrant_id = ww.warrant_id
                    WHERE oa.status IN ('ASSIGNED', 'IN_PROGRESS')
                ) ranked
                WHERE ranked.row_num = 1
            ) active_assignment ON active_assignment.officer_id = today_shift.officer_id
            ORDER BY today_shift.hours_logged DESC, o.name ASC
            """
        )
        on_duty_officers = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT
                oa.assignment_id,
                oa.task_type,
                oa.status,
                oa.priority,
                oa.sector_name,
                oa.assigned_at,
                oa.due_at,
                oa.notes,
                o.name AS officer_name,
                o.badge_number,
                CASE
                    WHEN cc.name IS NOT NULL THEN CONCAT('CRIMINAL: ', cc.name)
                    WHEN cs.case_id IS NOT NULL THEN CONCAT('CASE #', cs.case_id)
                    WHEN cr.crime_id IS NOT NULL THEN CONCAT('CRIME #', cr.crime_id)
                    WHEN ww.warrant_id IS NOT NULL THEN CONCAT('WARRANT #', ww.warrant_id)
                    ELSE 'GENERAL TASKING'
                END AS target_label
            FROM officers_assignment oa
            JOIN officers_officer o ON oa.officer_id = o.officer_id
            LEFT JOIN criminals_criminal cc ON oa.criminal_id = cc.criminal_id
            LEFT JOIN cases_case cs ON oa.case_id = cs.case_id
            LEFT JOIN crimes_crime cr ON oa.crime_id = cr.crime_id
            LEFT JOIN warrants_warrant ww ON oa.warrant_id = ww.warrant_id
            ORDER BY oa.assigned_at DESC, oa.assignment_id DESC
            LIMIT 20
            """
        )
        recent_assignments = dictfetchall(cursor)

    return render(request, 'officers/shift_tracking.html', {
        'shifts': shifts,
        'officers': officers,
        'criminals': criminals,
        'cases': cases,
        'sectors': sectors,
        'on_duty_officers': on_duty_officers,
        'recent_assignments': recent_assignments,
        'on_duty_count': len(on_duty_officers),
        'active_assignment_count': sum(1 for item in on_duty_officers if item.get('task_type')),
    })
