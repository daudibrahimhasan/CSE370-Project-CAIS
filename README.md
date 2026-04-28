# CAIS

Criminal Analysis & Investigation System (CAIS) is a Python + Django + MySQL database course project rebuilt in a flat, page-oriented style similar to the reference PHP project.

## Project Structure

Major pages now exist as top-level `.py` files, similar to the reference project's `.php` pages:

- `index.py`
- `features.py`
- `login.py`
- `dashboard.py`
- `OfficerSearch.py`
- `ShiftTracking.py`
- `CriminalList.py`
- `CriminalProfile.py`
- `CriminalRegistry.py`
- `RepeatOffenders.py`
- `CrimeList.py`
- `CrimeDetail.py`
- `CrimePatternFinder.py`
- `WarrantTracking.py`
- `BOLOList.py`
- `CaseRecords.py`
- `CaseDetail.py`
- `CourtCalendar.py`
- `CourtDetail.py`
- `connect.py`

## Database Folder

- `Database/project_database.sql`
  - reference-style SQL dump with CAIS schema and CAIS dummy data
- `Database/README.md`
  - reference-style numbered query explanation
- `Database/runtime_mysql_schema.sql`
  - Django runtime table mapping
- `Database/VIVA_PAGE_QUERY_MAP.md`
  - page-to-query guide for viva

## Feature Map

- `FEATURE_RUN_MAP.md`
  - tells you which feature is running from which `.py` file, route, and template

## Core Stack

- Frontend: HTML, CSS, JavaScript, Tailwind CDN
- Backend: Python, Django
- Database: MySQL
- Query Style: Raw SQL in feature page files

## Running Idea

The repository is intentionally structured so each major page has its own Python file, just like the reference project had one PHP file per feature.

Django is still used for:

- routing
- template rendering
- session handling

But the project is presented in a flat, feature-file style for easier demo and viva explanation.
