from django.contrib import messages
from django.db import connection
from django.shortcuts import redirect, render

from connect import dictfetchall, is_logged_in


def officer_search(request):
    if not is_logged_in(request):
        return redirect('admin_login')

    if request.method == 'POST':
        form_name = request.POST.get('form_name', '')

        with connection.cursor() as cursor:
            if form_name == 'add_team':
                team_name = request.POST.get('team_name', '').strip()
                if team_name:
                    cursor.execute(
                        """
                        INSERT INTO officers_team (team_name)
                        VALUES (%s)
                        """,
                        [team_name],
                    )
                    messages.success(request, "New team added successfully.")
                else:
                    messages.error(request, "Team name is required.")

            if form_name == 'add_officer':
                name = request.POST.get('name', '').strip()
                rank_name = request.POST.get('rank_name', '').strip()
                badge_number = request.POST.get('badge_number', '').strip()
                team_id = request.POST.get('assign_team_id', '').strip() or None

                if name and rank_name and badge_number:
                    cursor.execute(
                        """
                        INSERT INTO officers_officer (name, rank, badge_number, team_id)
                        VALUES (%s, %s, %s, %s)
                        """,
                        [name, rank_name, badge_number, team_id],
                    )
                    messages.success(request, "Officer added successfully.")
                else:
                    messages.error(request, "Officer name, rank, and badge number are required.")

        return redirect('officer_search')

    rank_query = request.GET.get('rank', '')
    team_query = request.GET.get('team', '')

    with connection.cursor() as cursor:
        query = """
            SELECT o.officer_id, o.name, o.rank, o.badge_number, t.team_name
            FROM officers_officer o
            LEFT JOIN officers_team t ON o.team_id = t.team_id
            WHERE 1=1
        """
        params = []
        if rank_query:
            query += " AND o.rank = %s"
            params.append(rank_query)
        if team_query:
            query += " AND o.team_id = %s"
            params.append(team_query)
        cursor.execute(query, params)
        officers = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT team_id, team_name
            FROM officers_team
            ORDER BY team_name
            """
        )
        teams = dictfetchall(cursor)

        cursor.execute(
            """
            SELECT DISTINCT rank
            FROM officers_officer
            ORDER BY rank
            """
        )
        ranks = [row['rank'] for row in dictfetchall(cursor)]

    return render(request, 'officers/officer_search.html', {
        'officers': officers,
        'teams': teams,
        'ranks': ranks,
        'selected_rank': rank_query,
        'selected_team': team_query,
    })
