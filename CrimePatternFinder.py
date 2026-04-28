from itertools import groupby

from django.db import connection
from django.shortcuts import redirect, render

from connect import dictfetchall, is_logged_in


def pattern_finder(request):
    if not is_logged_in(request):
        return redirect('admin_login')

    search_query = request.GET.get('method', '')
    results = []

    if search_query:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT crime_id, description, method_used, location, date_time, status
                FROM crimes_crime
                WHERE method_used LIKE %s
                ORDER BY method_used, date_time DESC
                """,
                [f"%{search_query}%"],
            )
            records = dictfetchall(cursor)

        records.sort(key=lambda x: x['method_used'])
        for method, group in groupby(records, key=lambda x: x['method_used']):
            results.append({'method': method, 'crimes': list(group)})

    return render(request, 'crimes/pattern_finder.html', {
        'search_query': search_query,
        'results': results,
    })
