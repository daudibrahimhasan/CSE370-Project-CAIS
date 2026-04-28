from django.contrib import messages
from django.db import connection
from django.http import Http404
from django.shortcuts import redirect, render

from connect import dictfetchall, dictfetchone, is_logged_in


def case_detail(request, case_id):
    if not is_logged_in(request):
        return redirect('admin_login')

    if request.method == 'POST':
        case_status = request.POST.get('case_status', '').strip()
        opened_date = request.POST.get('opened_date', '').strip() or None

        if case_status:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE cases_case
                    SET status = %s, opened_date = %s
                    WHERE case_id = %s
                    """,
                    [case_status, opened_date, case_id],
                )
            messages.success(request, "Case record updated successfully.")
        else:
            messages.error(request, "Case status is required.")

        return redirect('case_detail', case_id=case_id)

    with connection.cursor() as cursor:
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
        case = dictfetchone(cursor)
        if case is None:
            raise Http404("Case not found")

        cursor.execute(
            """
            SELECT court_id, court_date, judge_name
            FROM court_court
            WHERE case_id = %s
            ORDER BY court_date DESC
            """,
            [case_id],
        )
        court_dates = dictfetchall(cursor)

    return render(request, 'cases/case_detail.html', {
        'case': case,
        'court_dates': court_dates,
    })
