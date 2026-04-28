from django.db import connection
from django.shortcuts import redirect, render


def _dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def officer_search(request):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    rank_query = request.GET.get('rank', '')
    team_query = request.GET.get('team', '')

    with connection.cursor() as cursor:
        # Officer search page query: officer list with optional rank/team filters.
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
        officers = _dictfetchall(cursor)

        # Officer search page query: team dropdown options.
        cursor.execute(
            """
            SELECT team_id, team_name
            FROM officers_team
            ORDER BY team_name
            """
        )
        teams = _dictfetchall(cursor)

        # Officer search page query: distinct rank dropdown options.
        cursor.execute(
            """
            SELECT DISTINCT rank
            FROM officers_officer
            ORDER BY rank
            """
        )
        ranks = [row['rank'] for row in _dictfetchall(cursor)]

    return render(request, 'officers/officer_search.html', {
        'officers': officers,
        'teams': teams,
        'ranks': ranks,
        'selected_rank': rank_query,
        'selected_team': team_query,
    })


def shift_tracking(request):
    if not request.session.get('user_id'):
        return redirect('admin_login')

    with connection.cursor() as cursor:
        # Shift tracking page query: shifts joined with officer details.
        cursor.execute(
            """
            SELECT
                s.shift_id,
                s.date,
                s.hours_worked,
                o.officer_id,
                o.name AS officer_name,
                o.rank,
                o.badge_number
            FROM officers_shift s
            JOIN officers_officer o ON s.officer_id = o.officer_id
            ORDER BY s.date DESC, s.shift_id DESC
            """
        )
        shifts = _dictfetchall(cursor)

    return render(request, 'officers/shift_tracking.html', {'shifts': shifts})
