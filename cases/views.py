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


def case_status_list(request):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    status_filter = request.GET.get('status', '')

    with connection.cursor() as cursor:
        # Case list page query: cases joined with crime details, with optional status filter.
        query = """
            SELECT
                cs.case_id,
                cs.status,
                cs.opened_date,
                c.crime_id,
                c.location,
                c.description,
                c.method_used
            FROM cases_case cs
            JOIN crimes_crime c ON cs.crime_id = c.crime_id
        """
        params = []
        if status_filter:
            query += " WHERE cs.status = %s"
            params.append(status_filter)
        query += " ORDER BY cs.case_id DESC"
        cursor.execute(query, params)
        cases = _dictfetchall(cursor)

    return render(request, 'cases/case_list.html', {
        'cases': cases,
        'selected_status': status_filter,
    })


def case_detail(request, case_id):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        # Case detail page query: fetch one case and its linked crime information.
        cursor.execute(
            """
            SELECT
                cs.case_id,
                cs.status,
                cs.opened_date,
                c.crime_id,
                c.method_used,
                c.description,
                c.location
            FROM cases_case cs
            JOIN crimes_crime c ON cs.crime_id = c.crime_id
            WHERE cs.case_id = %s
            """,
            [case_id],
        )
        case = _dictfetchone(cursor)

        if case is None:
            raise Http404("Case not found")

        # Case detail page query: court dates linked to this case.
        cursor.execute(
            """
            SELECT court_id, court_date, judge_name
            FROM court_court
            WHERE case_id = %s
            ORDER BY court_date DESC
            """,
            [case_id],
        )
        court_dates = _dictfetchall(cursor)

    return render(request, 'cases/case_detail.html', {
        'case': case,
        'court_dates': court_dates,
    })
