from django.db import connection
from django.http import Http404
from django.shortcuts import redirect, render


def _dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def _dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def court_list(request):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    judge_filter = request.GET.get('judge', '').strip()

    with connection.cursor() as cursor:
        # Court list page query: court schedule joined with case and crime information.
        query = """
            SELECT
                ct.court_id,
                ct.court_date,
                ct.judge_name,
                cs.case_id,
                cs.status AS case_status,
                c.crime_id,
                c.method_used
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
        court_sessions = _dictfetchall(cursor)

    return render(request, 'court/court_list.html', {
        'court_sessions': court_sessions,
        'selected_judge': judge_filter,
    })


def court_detail(request, court_id):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        # Court detail page query: one hearing with its linked case and crime.
        cursor.execute(
            """
            SELECT
                ct.court_id,
                ct.court_date,
                ct.judge_name,
                cs.case_id,
                cs.status AS case_status,
                c.crime_id,
                c.description
            FROM court_court ct
            JOIN cases_case cs ON ct.case_id = cs.case_id
            JOIN crimes_crime c ON cs.crime_id = c.crime_id
            WHERE ct.court_id = %s
            """,
            [court_id],
        )
        court_session = _dictfetchone(cursor)

    if court_session is None:
        raise Http404("Court session not found")

    return render(request, 'court/court_detail.html', {'court_session': court_session})
