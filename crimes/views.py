from django.shortcuts import render, get_object_or_404
from django.db import connection
from .models import Crime, Victim, Evidence

def crime_list(request):
    crimes = Crime.objects.all().order_by('-date_time')
    return render(request, 'crimes/crime_list.html', {'crimes': crimes})

def crime_detail(request, crime_id):
    # Features 8, 12, 13
    crime = get_object_or_404(Crime, pk=crime_id)
    evidence_list = crime.evidence_items.all()
    victims = crime.victims_involved.prefetch_related('phones').all()
    criminals = crime.criminals_involved.all()
    
    return render(request, 'crimes/crime_detail.html', {
        'crime': crime,
        'evidence_list': evidence_list,
        'victims': victims,
        'criminals': criminals
    })

def pattern_finder(request):
    # Feature 1: SQL query with WHERE method_used LIKE or GROUP BY method_used
    search_query = request.GET.get('method', '')
    results = []
    
    if search_query:
        # Utilizing explicit custom SQL string to fulfill requirement
        with connection.cursor() as cursor:
            # Note: We group by method_used in application logic or use a raw query
            query = """
            SELECT crime_id, description, method_used, location, date_time, status
            FROM crimes_crime 
            WHERE method_used LIKE %s
            ORDER BY method_used, date_time DESC
            """
            like_param = f"%{search_query}%"
            cursor.execute(query, [like_param])
            
            columns = [col[0] for col in cursor.description]
            records = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Grouping records by method_used manually if grouping is needed
            from itertools import groupby
            records.sort(key=lambda x: x['method_used'])
            for method, group in groupby(records, key=lambda x: x['method_used']):
                results.append({
                    'method': method,
                    'crimes': list(group)
                })

    return render(request, 'crimes/pattern_finder.html', {
        'search_query': search_query,
        'results': results
    })
