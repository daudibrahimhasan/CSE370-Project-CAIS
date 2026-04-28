from django.contrib import messages
from django.db import connection
from django.http import Http404
from django.shortcuts import redirect, render

from connect import dictfetchall, dictfetchone, is_logged_in


def criminal_profile(request, criminal_id):
    if not is_logged_in(request):
        return redirect('admin_login')

    if request.method == 'POST':
        form_name = request.POST.get('form_name', '')

        with connection.cursor() as cursor:
            if form_name == 'add_nickname':
                alias = request.POST.get('alias', '').strip()
                if alias:
                    cursor.execute(
                        """
                        INSERT INTO criminals_nickname (criminal_id, alias)
                        VALUES (%s, %s)
                        """,
                        [criminal_id, alias],
                    )
                    messages.success(request, "Nickname added successfully.")
                else:
                    messages.error(request, "Alias is required.")

            if form_name == 'add_interrogation':
                officer_id = request.POST.get('officer_id', '').strip() or None
                interrogation_date = request.POST.get('interrogation_date', '').strip()
                notes = request.POST.get('notes', '').strip()
                if interrogation_date and notes:
                    cursor.execute(
                        """
                        INSERT INTO criminals_interrogation (officer_id, criminal_id, date, notes)
                        VALUES (%s, %s, %s, %s)
                        """,
                        [officer_id, criminal_id, interrogation_date, notes],
                    )
                    messages.success(request, "Interrogation note added successfully.")
                else:
                    messages.error(request, "Date and notes are required for interrogation log.")

        return redirect('criminal_profile', criminal_id=criminal_id)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                criminal_id,
                name,
                age,
                date_of_birth,
                gender,
                physical_description,
                is_repeat_offender,
                bounty_amount,
                sector_name,
                current_status,
                jail_name,
                jail_number
            FROM criminals_criminal
            WHERE criminal_id = %s
            """,
            [criminal_id],
        )
        criminal = dictfetchone(cursor)
        if criminal is None:
            raise Http404("Criminal not found")

        cursor.execute(
            """
            SELECT nickname_id, alias
            FROM criminals_nickname
            WHERE criminal_id = %s
            ORDER BY alias
            """,
            [criminal_id],
        )
        nicknames = dictfetchall(cursor)

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
        crimes = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT warrant_id, issue_date, status
            FROM warrants_warrant
            WHERE criminal_id = %s
            ORDER BY issue_date DESC
            """,
            [criminal_id],
        )
        warrants = dictfetchall(cursor)

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
        interrogations = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT officer_id, name, badge_number
            FROM officers_officer
            ORDER BY name
            """
        )
        officers = dictfetchall(cursor)

    return render(request, 'criminals/criminal_profile.html', {
        'criminal': criminal,
        'nicknames': nicknames,
        'crimes': crimes,
        'warrants': warrants,
        'interrogations': interrogations,
        'officers': officers,
    })
