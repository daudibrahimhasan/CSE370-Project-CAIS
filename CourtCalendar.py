from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render

from connect import dictfetchall, is_logged_in


def court_list(request):
    if not is_logged_in(request):
        return redirect('admin_login')

    if request.method == 'POST':
        case_id = request.POST.get('case_id', '').strip()
        court_date = request.POST.get('court_date', '').strip()
        judge_name = request.POST.get('judge_name', '').strip()

        if case_id and court_date and judge_name:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO court_court (case_id, court_date, judge_name)
                    VALUES (%s, %s, %s)
                    """,
                    [case_id, court_date, judge_name],
                )
            messages.success(request, "Court session added successfully.")
        else:
            messages.error(request, "Case, date, and judge are required.")

        return redirect('court_list')

    judge_filter = request.GET.get('judge', '').strip()

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT case_id, status
            FROM cases_case
            ORDER BY case_id DESC
            """
        )
        case_choices = dictfetchall(cursor)

        query = """
            SELECT
                ct.court_id,
                ct.court_date,
                ct.judge_name,
                ct.verdict,
                ct.sentence_type,
                cs.case_id,
                cs.status AS case_status,
                c.crime_id,
                c.method_used,
                CASE
                    WHEN ct.verdict = 'PENDING' THEN 'PENDING'
                    WHEN ct.sentence_type = 'PRISON' THEN 'IN JAIL'
                    WHEN ct.sentence_type = 'FINE' THEN 'FINED'
                    ELSE 'RELEASED'
                END AS verdict_label
            FROM court_court ct
            JOIN cases_case cs ON ct.case_id = cs.case_id
            JOIN crimes_crime c ON cs.crime_id = c.crime_id
        """
        params = []
        if judge_filter:
            query += " WHERE ct.judge_name LIKE %s"
            params.append(f"%{judge_filter}%")
        query += " ORDER BY ct.court_date ASC, ct.court_id ASC"
        cursor.execute(query, params)
        court_sessions = dictfetchall(cursor)
        
        cursor.execute(
            """
            SELECT DISTINCT judge_name
            FROM court_court
            ORDER BY judge_name ASC
            """
        )
        existing_judges = [row['judge_name'] for row in dictfetchall(cursor) if row['judge_name']]

    return render(request, 'court/court_list.html', {
        'court_sessions': court_sessions,
        'selected_judge': judge_filter,
        'case_choices': case_choices,
        'existing_judges': existing_judges,
    })
