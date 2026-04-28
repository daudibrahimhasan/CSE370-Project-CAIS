from django.shortcuts import redirect, render

from connect import is_logged_in, load_dashboard_stats


def dashboard(request):
    if not is_logged_in(request):
        return redirect('admin_login')

    context = load_dashboard_stats()
    context['session_username'] = request.session.get('username', 'Operator')
    return render(request, 'dashboard.html', context)
