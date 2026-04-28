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


def criminal_list(request):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        # Criminal list page query: show all registered criminals.
        cursor.execute(
            """
            SELECT criminal_id, name, age, gender
            FROM criminals_criminal
            ORDER BY name
            """
        )
        criminals = _dictfetchall(cursor)

    return render(request, 'criminals/criminal_list.html', {'criminals': criminals})


def criminal_profile(request, criminal_id):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        # Criminal profile page query: fetch the selected criminal.
        cursor.execute(
            """
            SELECT criminal_id, name, age, date_of_birth, gender, physical_description, is_repeat_offender
            FROM criminals_criminal
            WHERE criminal_id = %s
            """,
            [criminal_id],
        )
        criminal = _dictfetchone(cursor)
        if criminal is None:
            raise Http404("Criminal not found")

        # Criminal profile page query: aliases for this criminal.
        cursor.execute(
            """
            SELECT nickname_id, alias
            FROM criminals_nickname
            WHERE criminal_id = %s
            ORDER BY alias
            """,
            [criminal_id],
        )
        nicknames = _dictfetchall(cursor)

        # Criminal profile page query: crimes linked through crime involvement.
        cursor.execute(
            """
            SELECT c.crime_id, c.date_time, c.method_used
            FROM crimes_crime c
            JOIN crimes_crimeinvolvement ci ON c.crime_id = ci.crime_id
            WHERE ci.criminal_id = %s
            ORDER BY c.date_time DESC
            """,
            [criminal_id],
        )
        crimes = _dictfetchall(cursor)

        # Criminal profile page query: warrants issued for this criminal.
        cursor.execute(
            """
            SELECT warrant_id, issue_date, status
            FROM warrants_warrant
            WHERE criminal_id = %s
            ORDER BY issue_date DESC
            """,
            [criminal_id],
        )
        warrants = _dictfetchall(cursor)

        # Criminal profile page query: interrogation log with officer names.
        cursor.execute(
            """
            SELECT
                i.interrogation_id,
                i.date,
                i.notes,
                o.officer_id,
                o.name AS officer_name
            FROM criminals_interrogation i
            LEFT JOIN officers_officer o ON i.officer_id = o.officer_id
            WHERE i.criminal_id = %s
            ORDER BY i.date DESC
            """,
            [criminal_id],
        )
        interrogations = _dictfetchall(cursor)

    return render(request, 'criminals/criminal_profile.html', {
        'criminal': criminal,
        'nicknames': nicknames,
        'crimes': crimes,
        'warrants': warrants,
        'interrogations': interrogations,
    })


def repeat_offenders(request):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        # Repeat offenders page query: group crimes by criminal and keep counts >= 2.
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
        repeat_offenders_list = _dictfetchall(cursor)

    return render(request, 'criminals/repeat_offenders.html', {'offenders': repeat_offenders_list})


def criminal_registry(request):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        # Criminal registry page query: full registry with grouped offence descriptions.
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
        criminals = _dictfetchall(cursor)

    return render(request, 'criminals/criminal_registry.html', {'criminals': criminals})
