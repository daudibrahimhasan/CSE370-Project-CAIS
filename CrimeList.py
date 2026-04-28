from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render

from connect import dictfetchall, is_logged_in


def crime_list(request):
    if not is_logged_in(request):
        return redirect('admin_login')

    if request.method == 'POST':
        description = request.POST.get('description', '').strip()
        method_used = request.POST.get('method_used', '').strip()
        location = request.POST.get('location', '').strip()
        city = request.POST.get('city', '').strip() or None
        latitude = request.POST.get('latitude', '').strip() or None
        longitude = request.POST.get('longitude', '').strip() or None
        occurred_at = request.POST.get('occurred_at', '').strip()
        status = request.POST.get('status', '').strip() or 'Open'

        if description and method_used and location and occurred_at:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO crimes_crime (description, method_used, location, city, latitude, longitude, date_time, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [description, method_used, location, city, latitude, longitude, occurred_at, status],
                )
            messages.success(request, "Crime record added successfully.")
        else:
            messages.error(request, "Description, method, location, and date/time are required.")

        return redirect('crime_list')

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT crime_id, description, method_used, location, date_time, status
            FROM crimes_crime
            ORDER BY date_time DESC
            """
        )
        crimes = dictfetchall(cursor)

    return render(request, 'crimes/crime_list.html', {'crimes': crimes})
