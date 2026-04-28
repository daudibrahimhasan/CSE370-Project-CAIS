from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render

from connect import dictfetchall, is_logged_in


def criminal_list(request):
    if not is_logged_in(request):
        return redirect('admin_login')

    if request.method == 'POST':
        form_name = request.POST.get('form_name', '').strip()

        if form_name == 'update_bounty':
            criminal_id = request.POST.get('criminal_id', '').strip()
            bounty_amount = request.POST.get('bounty_amount', '').strip()

            if criminal_id and bounty_amount:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE criminals_criminal
                        SET bounty_amount = %s
                        WHERE criminal_id = %s
                        """,
                        [bounty_amount, criminal_id],
                    )
                messages.success(request, "Bounty updated successfully.")
            else:
                messages.error(request, "Criminal ID and bounty amount are required.")
        else:
            name = request.POST.get('name', '').strip()
            age = request.POST.get('age', '').strip()
            date_of_birth = request.POST.get('date_of_birth', '').strip() or None
            gender = request.POST.get('gender', '').strip()
            physical_description = request.POST.get('physical_description', '').strip()
            bounty_amount = request.POST.get('bounty_amount', '').strip() or '0.00'

            if name and age and gender and physical_description:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO criminals_criminal (
                            name, age, date_of_birth, gender, physical_description, is_repeat_offender, bounty_amount
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        [name, age, date_of_birth, gender, physical_description, 0, bounty_amount],
                    )
                messages.success(request, "Criminal profile created successfully.")
            else:
                messages.error(request, "Name, age, gender, and physical description are required.")

        return redirect('criminal_list')

    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT criminal_id, name, age, gender, bounty_amount
            FROM criminals_criminal
            ORDER BY name
            """
        )
        criminals = dictfetchall(cursor)

    return render(request, 'criminals/criminal_list.html', {'criminals': criminals})
