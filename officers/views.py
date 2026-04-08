from django.shortcuts import render
from django.db import connection
from .models import Officer, Shift, Team

def officer_search(request):
    # Feature 5: Search officers by rank or team. A search/filter page with a dropdown for rank and team. 
    # SQL uses WHERE rank = and/or team_id =.
    
    rank_query = request.GET.get('rank', '')
    team_query = request.GET.get('team', '')
    
    officers = []
    
    # We will use raw SQL to satisfy "SQL uses WHERE rank = and/or team_id ="
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
        columns = [col[0] for col in cursor.description]
        officers = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    teams = Team.objects.all()
    # Get unique ranks for dropdown
    # Use ORM just to populate the form options
    ranks = Officer.objects.values_list('rank', flat=True).distinct()
    
    return render(request, 'officers/officer_search.html', {
        'officers': officers,
        'teams': teams,
        'ranks': ranks,
        'selected_rank': rank_query,
        'selected_team': team_query
    })

def shift_tracking(request):
    # Feature 3: Officer shift tracking: A simple page showing which officer worked on which date, pulled from Shift table.
    shifts = Shift.objects.select_related('officer').all().order_by('-date')
    return render(request, 'officers/shift_tracking.html', {'shifts': shifts})
