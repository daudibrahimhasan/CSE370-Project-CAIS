# CAIS Feature Run Map

This file shows where each visible feature is running from in the rebuilt Python project.

## Public Pages

- Home page
  - Route: `/`
  - Python file: `index.py`
  - Function: `home`
  - Template: `templates/admin_auth/features.html`

- Features page
  - Route: `/features/`
  - Python file: `features.py`
  - Function: `features_page`
  - Template: `templates/admin_auth/features.html`

- Login page
  - Route: `/login/`
  - Python file: `login.py`
  - Function: `admin_login`
  - Template: `templates/admin_auth/login.html`

- Logout page
  - Route: `/logout/`
  - Python file: `login.py`
  - Function: `admin_logout`

## Dashboard

- Dashboard
  - Route: `/dashboard/`
  - Python file: `dashboard.py`
  - Function: `dashboard`
  - Template: `templates/dashboard.html`

## Officer Features

- Officer search
  - Route: `/officers/search/`
  - Python file: `OfficerSearch.py`
  - Function: `officer_search`
  - Template: `templates/officers/officer_search.html`

- Shift tracking
  - Route: `/officers/shifts/`
  - Python file: `ShiftTracking.py`
  - Function: `shift_tracking`
  - Template: `templates/officers/shift_tracking.html`

## Criminal Features

- Criminal list
  - Route: `/criminals/`
  - Python file: `CriminalList.py`
  - Function: `criminal_list`
  - Template: `templates/criminals/criminal_list.html`

- Criminal profile
  - Route: `/criminals/<criminal_id>/`
  - Python file: `CriminalProfile.py`
  - Function: `criminal_profile`
  - Template: `templates/criminals/criminal_profile.html`

- Criminal registry
  - Route: `/criminals/registry/`
  - Python file: `CriminalRegistry.py`
  - Function: `criminal_registry`
  - Template: `templates/criminals/criminal_registry.html`

- Repeat offender alert
  - Route: `/criminals/repeat-offenders/`
  - Python file: `RepeatOffenders.py`
  - Function: `repeat_offenders`
  - Template: `templates/criminals/repeat_offenders.html`

## Crime Features

- Crime list
  - Route: `/crimes/`
  - Python file: `CrimeList.py`
  - Function: `crime_list`
  - Template: `templates/crimes/crime_list.html`

- Crime detail
  - Route: `/crimes/<crime_id>/`
  - Python file: `CrimeDetail.py`
  - Function: `crime_detail`
  - Template: `templates/crimes/crime_detail.html`

- Crime pattern finder
  - Route: `/crimes/pattern-finder/`
  - Python file: `CrimePatternFinder.py`
  - Function: `pattern_finder`
  - Template: `templates/crimes/pattern_finder.html`

## Warrant Features

- Warrant tracking
  - Route: `/warrants/`
  - Python file: `WarrantTracking.py`
  - Function: `warrant_tracking`
  - Template: `templates/warrants/warrant_tracking.html`

- BOLO list
  - Route: `/warrants/bolo/`
  - Python file: `BOLOList.py`
  - Function: `bolo_list`
  - Template: `templates/warrants/bolo_list.html`

## Case Features

- Case records
  - Route: `/cases/`
  - Python file: `CaseRecords.py`
  - Function: `case_status_list`
  - Template: `templates/cases/case_list.html`

- Case detail
  - Route: `/cases/<case_id>/`
  - Python file: `CaseDetail.py`
  - Function: `case_detail`
  - Template: `templates/cases/case_detail.html`

## Court Features

- Court calendar
  - Route: `/court/`
  - Python file: `CourtCalendar.py`
  - Function: `court_list`
  - Template: `templates/court/court_list.html`

- Court detail
  - Route: `/court/<court_id>/`
  - Python file: `CourtDetail.py`
  - Function: `court_detail`
  - Template: `templates/court/court_detail.html`

## Shared File

- Shared helper file
  - Python file: `connect.py`
  - Purpose:
    - shared database cursor row conversion
    - login/session check
    - public features page content
    - dashboard summary counts
