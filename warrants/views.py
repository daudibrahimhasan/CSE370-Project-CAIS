from django.shortcuts import render
from django.db import connection
from .models import Warrant

def warrant_tracking(request):
    # Feature 9: Warrants page showing all warrants with their status. Filterable by Active or Cancelled.
    status_filter = request.GET.get('status', '')
    
    if status_filter:
        warrants = Warrant.objects.filter(status=status_filter).select_related('criminal').order_by('-issue_date')
    else:
        warrants = Warrant.objects.select_related('criminal').all().order_by('-issue_date')
        
    return render(request, 'warrants/warrant_tracking.html', {
        'warrants': warrants,
        'selected_status': status_filter
    })

def bolo_list(request):
    # Feature 11: BOLO list querying all warrants WHERE status = 'Active' and showing the linked criminal's name and details.
    bolo_criminals = []
    
    # Requirement: A page that queries all warrants WHERE status = 'Active' and shows the linked criminal's name and details.
    # Using explicit SQL query
    with connection.cursor() as cursor:
        query = """
            SELECT w.warrant_id, w.issue_date, c.criminal_id, c.name, c.age, c.gender, c.physical_description
            FROM warrants_warrant w
            JOIN criminals_criminal c ON w.criminal_id = c.criminal_id
            WHERE w.status = 'Active'
            ORDER BY w.issue_date DESC
        """
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        bolo_criminals = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
    return render(request, 'warrants/bolo_list.html', {'bolos': bolo_criminals})
