from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db import connection
from django.shortcuts import redirect, render


def _dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def _is_logged_in(request):
    return bool(request.session.get('user_id'))


def _load_dashboard_stats():
    with connection.cursor() as cursor:
        # Dashboard card query: total number of crime records.
        cursor.execute("SELECT COUNT(*) AS total_crimes FROM crimes_crime")
        total_crimes = _dictfetchone(cursor)['total_crimes']

        # Dashboard card query: active warrants count.
        cursor.execute(
            """
            SELECT COUNT(*) AS active_warrants
            FROM warrants_warrant
            WHERE status = %s
            """,
            ['Active'],
        )
        active_warrants = _dictfetchone(cursor)['active_warrants']

        # Dashboard card query: open cases count.
        cursor.execute(
            """
            SELECT COUNT(*) AS open_cases
            FROM cases_case
            WHERE status = %s
            """,
            ['Open'],
        )
        open_cases = _dictfetchone(cursor)['open_cases']

        # Dashboard card query: repeat offenders based on crime involvement count.
        cursor.execute(
            """
            SELECT COUNT(*) AS repeat_offenders_count
            FROM (
                SELECT ci.criminal_id
                FROM crimes_crimeinvolvement ci
                GROUP BY ci.criminal_id
                HAVING COUNT(ci.crime_id) >= 2
            ) repeat_scan
            """
        )
        repeat_offenders_count = _dictfetchone(cursor)['repeat_offenders_count']

    return {
        'total_crimes': total_crimes,
        'active_warrants': active_warrants,
        'open_cases': open_cases,
        'repeat_offenders_count': repeat_offenders_count,
    }

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        with connection.cursor() as cursor:
            # Login page query: fetch one operator by username for password verification.
            cursor.execute(
                """
                SELECT id, username, password, role, is_active
                FROM admin_auth_adminuser
                WHERE username = %s
                LIMIT 1
                """,
                [username],
            )
            user = _dictfetchone(cursor)

        if user and user['is_active'] and check_password(password, user['password']):
            request.session['user_id'] = user['id']
            request.session['username'] = user['username']
            request.session['role'] = user.get('role') or 'Viewer'
            messages.success(request, f"You are now logged in as {username}.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'admin_auth/login.html')

def admin_logout(request):
    request.session.flush()
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

def home(request):
    if _is_logged_in(request):
        return redirect('dashboard')
    return render(request, 'admin_auth/features.html', _public_feature_context())


def _public_feature_context():
    return {
        'unique_features': [
            {
                'title': 'Crime Pattern Finder',
                'summary': 'A smart search that groups crimes committed using the same method or trick.',
                'details': 'Investigators can search by method of operation and quickly see likely linked incidents.',
            },
            {
                'title': 'Repeat Offender Alert',
                'summary': 'A live alert that counts criminal involvement records and highlights repeat offenders.',
                'details': 'The system uses grouped SQL counts to mark suspects with multiple crime records.',
            },
        ],
        'feature_sections': [
            {
                'heading': 'Officer Management',
                'items': [
                    'Keep a list of police officers with name, rank, and badge number.',
                    'Assign officers to teams such as Narcotics or Traffic.',
                    'Record which officer worked on which day and for how many hours.',
                    'Quickly search officers by rank or team.',
                ],
            },
            {
                'heading': 'Criminal Tracking',
                'items': [
                    'Store criminal information such as name, age, date of birth, gender, and physical description.',
                    'Save multiple nicknames or street names for each criminal.',
                    'Write interrogation notes for questioning history.',
                    'Track active or cancelled arrest warrants.',
                    'Generate a BOLO list for criminals with active warrants.',
                ],
            },
            {
                'heading': 'Crime Investigation',
                'items': [
                    'Record each crime with description, method, location, city, date, and status.',
                    'Link evidence such as guns, phones, laptops, and other items to a crime.',
                    'Connect victim names and phone numbers to each crime.',
                    'Track which criminal was involved in which crime.',
                    'Track which officer investigated which crime.',
                ],
            },
            {
                'heading': 'Case And Court Monitoring',
                'items': [
                    'Mark cases as still open or finished.',
                    'Track court dates and judge names for each case.',
                    'Show case details together with linked crime and court information.',
                ],
            },
            {
                'heading': 'Admin Control',
                'items': [
                    'Allow only admin users to log in and access the system.',
                    'Use MySQL as the backend database and raw SQL inside the feature views.',
                ],
            },
        ],
    }


def features(request):
    if _is_logged_in(request):
        return redirect('dashboard')
    return render(request, 'admin_auth/features.html', _public_feature_context())

def dashboard(request):
    if not _is_logged_in(request):
        return redirect('admin_login')

    context = _load_dashboard_stats()
    context['session_username'] = request.session.get('username', 'Operator')
    return render(request, 'dashboard.html', context)
