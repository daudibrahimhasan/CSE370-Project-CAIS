from django.db import connection
from django.shortcuts import redirect, render


def _dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def warrant_tracking(request):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    status_filter = request.GET.get('status', '')

    with connection.cursor() as cursor:
        # Warrant tracking page query: warrants joined with criminal names, with optional status filter.
        query = """
            SELECT
                w.warrant_id,
                w.issue_date,
                w.status,
                c.criminal_id,
                c.name AS criminal_name
            FROM warrants_warrant w
            JOIN criminals_criminal c ON w.criminal_id = c.criminal_id
        """
        params = []
        if status_filter:
            query += " WHERE w.status = %s"
            params.append(status_filter)
        query += " ORDER BY w.issue_date DESC, w.warrant_id DESC"
        cursor.execute(query, params)
        warrants = _dictfetchall(cursor)

    return render(request, 'warrants/warrant_tracking.html', {
        'warrants': warrants,
        'selected_status': status_filter,
    })


def bolo_list(request):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        # BOLO page query: only active warrants with suspect details.
        cursor.execute(
            """
            SELECT w.warrant_id, w.issue_date, c.criminal_id, c.name, c.age, c.gender, c.physical_description
            FROM warrants_warrant w
            JOIN criminals_criminal c ON w.criminal_id = c.criminal_id
            WHERE w.status = 'Active'
            ORDER BY w.issue_date DESC
            """
        )
        bolo_criminals = _dictfetchall(cursor)

    return render(request, 'warrants/bolo_list.html', {'bolos': bolo_criminals})
