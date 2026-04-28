from django.db import connection


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def dictfetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


def is_logged_in(request):
    return bool(request.session.get('user_id'))


def require_login(request):
    return not is_logged_in(request)


def public_feature_context():
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
                'page_file': 'OfficerSearch.py',
                'route': '/officers/search/',
                'items': [
                    'Keep a list of police officers with name, rank, and badge number.',
                    'Assign officers to teams such as Narcotics or Traffic.',
                    'Record which officer worked on which day and for how many hours.',
                    'Quickly search officers by rank or team.',
                ],
            },
            {
                'heading': 'Criminal Tracking',
                'page_file': 'CriminalList.py',
                'route': '/criminals/',
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
                'page_file': 'CrimeList.py',
                'route': '/crimes/',
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
                'page_file': 'CaseRecords.py',
                'route': '/cases/',
                'items': [
                    'Mark cases as still open or finished.',
                    'Track court dates and judge names for each case.',
                    'Show case details together with linked crime and court information.',
                ],
            },
            {
                'heading': 'Admin Control',
                'page_file': 'login.py',
                'route': '/login/',
                'items': [
                    'Allow only admin users to log in and access the system.',
                    'Use MySQL as the backend database and raw SQL inside the feature pages.',
                ],
            },
        ],
        'feature_pages': [
            {'title': 'Public Feature Overview', 'page_file': 'features.py', 'route_name': 'features', 'route_path': '/features/', 'summary': 'Shows the complete module list and unique features before login.'},
            {'title': 'Admin Login', 'page_file': 'login.py', 'route_name': 'admin_login', 'route_path': '/login/', 'summary': 'Checks the admin_auth_adminuser table with a raw SQL SELECT query.'},
            {'title': 'Dashboard', 'page_file': 'dashboard.py', 'route_name': 'dashboard', 'route_path': '/dashboard/', 'summary': 'Loads live summary counts for crimes, warrants, cases, and repeat offenders.'},
            {'title': 'Officer Search', 'page_file': 'OfficerSearch.py', 'route_name': 'officer_search', 'route_path': '/officers/search/', 'summary': 'Runs officer, team, and rank queries and supports adding teams and officers.'},
            {'title': 'Shift Tracking', 'page_file': 'ShiftTracking.py', 'route_name': 'shift_tracking', 'route_path': '/officers/shifts/', 'summary': 'Stores officer work logs and shows shift history with officer details.'},
            {'title': 'Criminal List', 'page_file': 'CriminalList.py', 'route_name': 'criminal_list', 'route_path': '/criminals/', 'summary': 'Creates criminal profiles and lists all registered subjects.'},
            {'title': 'Criminal Registry', 'page_file': 'CriminalRegistry.py', 'route_name': 'criminal_registry', 'route_path': '/criminals/registry/', 'summary': 'Shows grouped offence history for every criminal in one page.'},
            {'title': 'Repeat Offender Alert', 'page_file': 'RepeatOffenders.py', 'route_name': 'repeat_offenders', 'route_path': '/criminals/repeat-offenders/', 'summary': 'Counts crime links per criminal and highlights repeat offenders.'},
            {'title': 'Crime Records', 'page_file': 'CrimeList.py', 'route_name': 'crime_list', 'route_path': '/crimes/', 'summary': 'Creates crime records and lists every logged incident.'},
            {'title': 'Crime Pattern Finder', 'page_file': 'CrimePatternFinder.py', 'route_name': 'pattern_finder', 'route_path': '/crimes/pattern-finder/', 'summary': 'Searches crimes by method_used to find repeated tricks or patterns.'},
            {'title': 'Warrant Tracking', 'page_file': 'WarrantTracking.py', 'route_name': 'warrant_tracking', 'route_path': '/warrants/', 'summary': 'Creates and filters warrants by status using raw SQL.'},
            {'title': 'BOLO List', 'page_file': 'BOLOList.py', 'route_name': 'bolo_list', 'route_path': '/warrants/bolo/', 'summary': 'Lists only criminals with active warrants for quick field review.'},
            {'title': 'Case Records', 'page_file': 'CaseRecords.py', 'route_name': 'case_status_list', 'route_path': '/cases/', 'summary': 'Creates cases from crimes and filters open or finished case files.'},
            {'title': 'Court Calendar', 'page_file': 'CourtCalendar.py', 'route_name': 'court_list', 'route_path': '/court/', 'summary': 'Creates court sessions and lists judge, date, and linked case details.'},
        ],
    }


def load_dashboard_stats():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS total_crimes FROM crimes_crime")
        total_crimes = dictfetchone(cursor)['total_crimes']

        cursor.execute(
            """
            SELECT COUNT(*) AS active_warrants
            FROM warrants_warrant
            WHERE status = %s
            """,
            ['Active'],
        )
        active_warrants = dictfetchone(cursor)['active_warrants']

        cursor.execute(
            """
            SELECT COUNT(*) AS open_cases
            FROM cases_case
            WHERE status = %s
            """,
            ['Open'],
        )
        open_cases = dictfetchone(cursor)['open_cases']

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
        repeat_offenders_count = dictfetchone(cursor)['repeat_offenders_count']

    return {
        'total_crimes': total_crimes,
        'active_warrants': active_warrants,
        'open_cases': open_cases,
        'repeat_offenders_count': repeat_offenders_count,
    }
