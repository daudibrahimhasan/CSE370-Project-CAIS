from django.contrib import messages
from django.db import connection
from django.http import Http404
from django.shortcuts import redirect, render

from connect import dictfetchall, dictfetchone, is_logged_in


def crime_detail(request, crime_id):
    if not is_logged_in(request):
        return redirect('admin_login')

    if request.method == 'POST':
        form_name = request.POST.get('form_name', '')

        with connection.cursor() as cursor:
            if form_name == 'add_evidence':
                evidence_type = request.POST.get('evidence_type', '').strip()
                description = request.POST.get('evidence_description', '').strip()
                if evidence_type and description:
                    cursor.execute(
                        """
                        INSERT INTO crimes_evidence (crime_id, type, description)
                        VALUES (%s, %s, %s)
                        """,
                        [crime_id, evidence_type, description],
                    )
                    messages.success(request, "Evidence added successfully.")
                else:
                    messages.error(request, "Evidence type and description are required.")

            if form_name == 'add_victim':
                victim_name = request.POST.get('victim_name', '').strip()
                victim_phone = request.POST.get('victim_phone', '').strip()
                if victim_name:
                    cursor.execute(
                        """
                        INSERT INTO crimes_victim (name)
                        VALUES (%s)
                        """,
                        [victim_name],
                    )
                    victim_id = cursor.lastrowid
                    cursor.execute(
                        """
                        INSERT INTO crimes_crimevictim (crime_id, victim_id)
                        VALUES (%s, %s)
                        """,
                        [crime_id, victim_id],
                    )
                    if victim_phone:
                        cursor.execute(
                            """
                            INSERT INTO crimes_victimphone (victim_id, phone_number)
                            VALUES (%s, %s)
                            """,
                            [victim_id, victim_phone],
                        )
                    messages.success(request, "Victim linked successfully.")
                else:
                    messages.error(request, "Victim name is required.")

            if form_name == 'add_criminal_link':
                criminal_id = request.POST.get('criminal_id', '').strip()
                if criminal_id:
                    cursor.execute(
                        """
                        INSERT IGNORE INTO crimes_crimeinvolvement (criminal_id, crime_id)
                        VALUES (%s, %s)
                        """,
                        [criminal_id, crime_id],
                    )
                    messages.success(request, "Criminal linked to crime.")
                else:
                    messages.error(request, "Select a criminal to link.")

            if form_name == 'add_officer_link':
                officer_id = request.POST.get('officer_id', '').strip()
                work_date = request.POST.get('work_date', '').strip()
                if officer_id and work_date:
                    cursor.execute(
                        """
                        INSERT IGNORE INTO crimes_investigates (officer_id, crime_id, date_worked)
                        VALUES (%s, %s, %s)
                        """,
                        [officer_id, crime_id, work_date],
                    )
                    messages.success(request, "Officer linked to investigation.")
                else:
                    messages.error(request, "Officer and work date are required.")

        return redirect('crime_detail', crime_id=crime_id)

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT crime_id, description, method_used, location, date_time, status
            FROM crimes_crime
            WHERE crime_id = %s
            """,
            [crime_id],
        )
        crime = dictfetchone(cursor)
        if crime is None:
            raise Http404("Crime not found")

        cursor.execute(
            """
            SELECT evidence_id, type, description
            FROM crimes_evidence
            WHERE crime_id = %s
            ORDER BY evidence_id
            """,
            [crime_id],
        )
        evidence_list = dictfetchall(cursor)

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
        victims = dictfetchall(cursor)

        for victim in victims:
            cursor.execute(
                """
                SELECT phone_id, phone_number
                FROM crimes_victimphone
                WHERE victim_id = %s
                ORDER BY phone_id
                """,
                [victim['victim_id']],
            )
            victim['phones'] = dictfetchall(cursor)

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
        criminals = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT criminal_id, name
            FROM criminals_criminal
            ORDER BY name
            """
        )
        criminal_choices = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT officer_id, name, badge_number
            FROM officers_officer
            ORDER BY name
            """
        )
        officer_choices = dictfetchall(cursor)

    return render(request, 'crimes/crime_detail.html', {
        'crime': crime,
        'evidence_list': evidence_list,
        'victims': victims,
        'criminals': criminals,
        'criminal_choices': criminal_choices,
        'officer_choices': officer_choices,
    })
