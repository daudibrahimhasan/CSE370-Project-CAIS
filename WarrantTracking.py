from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render

from connect import dictfetchall, is_logged_in


def warrant_tracking(request):
    if not is_logged_in(request):
        return redirect('admin_login')

    if request.method == 'POST':
        criminal_id = request.POST.get('criminal_id', '').strip()
        issue_date = request.POST.get('issue_date', '').strip()
        status = request.POST.get('status', '').strip() or 'Active'

        if criminal_id and issue_date:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO warrants_warrant (criminal_id, issue_date, status)
                    VALUES (%s, %s, %s)
                    """,
                    [criminal_id, issue_date, status],
                )
            messages.success(request, "Warrant added successfully.")
        else:
            messages.error(request, "Criminal and issue date are required.")

        return redirect('warrant_tracking')

    status_filter = request.GET.get('status', '')

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT criminal_id, name
            FROM criminals_criminal
            ORDER BY name
            """
        )
        criminal_choices = dictfetchall(cursor)

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
        warrants = dictfetchall(cursor)

    return render(request, 'warrants/warrant_tracking.html', {
        'warrants': warrants,
        'selected_status': status_filter,
        'criminal_choices': criminal_choices,
    })
