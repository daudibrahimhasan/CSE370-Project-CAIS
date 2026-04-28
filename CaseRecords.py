from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render

from connect import dictfetchall, is_logged_in


def case_status_list(request):
    if not is_logged_in(request):
        return redirect('admin_login')

    if request.method == 'POST':
        crime_id = request.POST.get('crime_id', '').strip()
        case_status = request.POST.get('case_status', '').strip() or 'Open'
        opened_date = request.POST.get('opened_date', '').strip() or None

        if crime_id:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO cases_case (crime_id, status, opened_date)
                    VALUES (%s, %s, %s)
                    """,
                    [crime_id, case_status, opened_date],
                )
            messages.success(request, "Case record created successfully.")
        else:
            messages.error(request, "Crime selection is required.")

        return redirect('case_status_list')

    status_filter = request.GET.get('status', '')

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT c.crime_id, c.method_used, c.location
            FROM crimes_crime c
            LEFT JOIN cases_case cs ON c.crime_id = cs.crime_id
            WHERE cs.case_id IS NULL
            ORDER BY c.date_time DESC
            """
        )
        available_crimes = dictfetchall(cursor)

        query = """
            SELECT
                cs.case_id,
                cs.status,
                cs.opened_date,
                c.crime_id,
                c.location,
                c.description,
                c.method_used,
                latest_court.verdict_label
            FROM cases_case cs
            JOIN crimes_crime c ON cs.crime_id = c.crime_id
            LEFT JOIN (
                SELECT
                    ranked.case_id,
                    CASE
                        WHEN ranked.verdict = 'PENDING' THEN 'PENDING'
                        WHEN ranked.sentence_type = 'PRISON' THEN 'IN JAIL'
                        WHEN ranked.sentence_type = 'FINE' THEN 'FINED'
                        ELSE 'RELEASED'
                    END AS verdict_label
                FROM (
                    SELECT
                        ct.case_id,
                        ct.verdict,
                        ct.sentence_type,
                        ROW_NUMBER() OVER (
                            PARTITION BY ct.case_id
                            ORDER BY ct.court_date DESC, ct.court_id DESC
                        ) AS row_num
                    FROM court_court ct
                ) ranked
                WHERE ranked.row_num = 1
            ) latest_court ON latest_court.case_id = cs.case_id
        """
        params = []
        if status_filter:
            query += " WHERE cs.status = %s"
            params.append(status_filter)
        query += " ORDER BY cs.case_id DESC"
        cursor.execute(query, params)
        cases = dictfetchall(cursor)

    return render(request, 'cases/case_list.html', {
        'cases': cases,
        'selected_status': status_filter,
        'available_crimes': available_crimes,
    })
