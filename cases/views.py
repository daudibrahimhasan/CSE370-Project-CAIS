from django.shortcuts import render, get_object_or_404
from .models import Case

def case_status_list(request):
    # Feature 15: Case status: Cases are marked Open or Finished. A cases page shows all cases with a filter by status.
    status_filter = request.GET.get('status', '')
    
    if status_filter:
        cases = Case.objects.filter(status=status_filter).select_related('crime').order_by('-case_id')
    else:
        cases = Case.objects.select_related('crime').all().order_by('-case_id')
        
    return render(request, 'cases/case_list.html', {
        'cases': cases,
        'selected_status': status_filter
    })

def case_detail(request, case_id):
    # Feature 14: Court dates: Each case page shows all court sessions with dates and judge names from the Court table.
    case = get_object_or_404(Case.objects.select_related('crime'), pk=case_id)
    court_dates = case.court_dates.all().order_by('-court_date')
    
    return render(request, 'cases/case_detail.html', {
        'case': case,
        'court_dates': court_dates
    })
