from django.db import connection
from django.http import Http404
from django.shortcuts import redirect, render

from connect import dictfetchone, is_logged_in


def court_detail(request, court_id):
    if not is_logged_in(request):
        return redirect('admin_login')

    with connection.cursor() as cursor:
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
        court_session = dictfetchone(cursor)

    if court_session is None:
        raise Http404("Court session not found")

    return render(request, 'court/court_detail.html', {'court_session': court_session})
