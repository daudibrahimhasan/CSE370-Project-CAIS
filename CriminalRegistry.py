from django.db import connection
from django.shortcuts import redirect, render

from connect import dictfetchall, is_logged_in


def criminal_registry(request):
    if not is_logged_in(request):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                c.criminal_id,
                c.name,
                c.age,
                c.gender,
                c.is_repeat_offender,
                GROUP_CONCAT(cr.description ORDER BY cr.date_time DESC SEPARATOR ', ') AS offences
            FROM criminals_criminal c
            LEFT JOIN crimes_crimeinvolvement ci ON c.criminal_id = ci.criminal_id
            LEFT JOIN crimes_crime cr ON ci.crime_id = cr.crime_id
            GROUP BY c.criminal_id, c.name, c.age, c.gender, c.is_repeat_offender
            ORDER BY c.name
            """
        )
        criminals = dictfetchall(cursor)

    return render(request, 'criminals/criminal_registry.html', {'criminals': criminals})
