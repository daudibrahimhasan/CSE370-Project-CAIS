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


def crime_list(request):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        # Crime list page query: show all crimes for the main records table.
        cursor.execute(
            """
            SELECT crime_id, description, method_used, location, date_time, status
            FROM crimes_crime
            ORDER BY date_time DESC
            """
        )
        crimes = _dictfetchall(cursor)

    return render(request, 'crimes/crime_list.html', {'crimes': crimes})


def crime_detail(request, crime_id):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        # Crime detail page query: fetch the selected crime.
        cursor.execute(
            """
            SELECT crime_id, description, method_used, location, date_time, status
            FROM crimes_crime
            WHERE crime_id = %s
            """,
            [crime_id],
        )
        crime = _dictfetchone(cursor)
        if crime is None:
            raise Http404("Crime not found")

        # Crime detail page query: evidence linked to this crime.
        cursor.execute(
            """
            SELECT evidence_id, type, description
            FROM crimes_evidence
            WHERE crime_id = %s
            ORDER BY evidence_id
            """,
            [crime_id],
        )
        evidence_list = _dictfetchall(cursor)

        # Crime detail page query: victims linked through the junction table.
        cursor.execute(
            """
            SELECT DISTINCT v.victim_id, v.name
            FROM crimes_victim v
            JOIN crimes_crimevictim cv ON v.victim_id = cv.victim_id
            WHERE cv.crime_id = %s
            ORDER BY v.name
            """,
            [crime_id],
        )
        victims = _dictfetchall(cursor)

        for victim in victims:
            # Crime detail page query: phone numbers for one victim.
            cursor.execute(
                """
                SELECT phone_id, phone_number
                FROM crimes_victimphone
                WHERE victim_id = %s
                ORDER BY phone_id
                """,
                [victim['victim_id']],
            )
            victim['phones'] = _dictfetchall(cursor)

        # Crime detail page query: criminals involved in this crime.
        cursor.execute(
            """
            SELECT c.criminal_id, c.name
            FROM criminals_criminal c
            JOIN crimes_crimeinvolvement ci ON c.criminal_id = ci.criminal_id
            WHERE ci.crime_id = %s
            ORDER BY c.name
            """,
            [crime_id],
        )
        criminals = _dictfetchall(cursor)

    return render(request, 'crimes/crime_detail.html', {
        'crime': crime,
        'evidence_list': evidence_list,
        'victims': victims,
        'criminals': criminals,
    })


def pattern_finder(request):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    search_query = request.GET.get('method', '')
    results = []

    if search_query:
        with connection.cursor() as cursor:
            # Pattern finder page query: crimes with similar method of operation.
            cursor.execute(
                """
                SELECT crime_id, description, method_used, location, date_time, status
                FROM crimes_crime
                WHERE method_used LIKE %s
                ORDER BY method_used, date_time DESC
                """,
                [f"%{search_query}%"],
            )
            records = _dictfetchall(cursor)

        from itertools import groupby

        records.sort(key=lambda x: x['method_used'])
        for method, group in groupby(records, key=lambda x: x['method_used']):
            results.append({
                'method': method,
                'crimes': list(group),
            })

    return render(request, 'crimes/pattern_finder.html', {
        'search_query': search_query,
        'results': results,
    })
