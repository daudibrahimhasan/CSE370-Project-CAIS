from django.db import connection
from django.shortcuts import redirect, render

from connect import dictfetchall, is_logged_in


def repeat_offenders(request):
    if not is_logged_in(request):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT c.criminal_id, c.name, COUNT(ci.crime_id) AS crime_count
            FROM criminals_criminal c
            JOIN crimes_crimeinvolvement ci ON c.criminal_id = ci.criminal_id
            GROUP BY c.criminal_id, c.name
            HAVING COUNT(ci.crime_id) >= 2
            ORDER BY crime_count DESC
            """
        )
        offenders = dictfetchall(cursor)

    return render(request, 'criminals/repeat_offenders.html', {'offenders': offenders})
