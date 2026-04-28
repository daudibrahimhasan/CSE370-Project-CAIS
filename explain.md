# C.A.I.S. Detailed Feature Map

This document breaks down exactly what happens under the hood when you click a button or perform an action in the frontend. It maps the frontend interaction directly to the backend Python file and the raw SQL query executed in MariaDB.

---

### 1. Keep a list of police officers
*   **Frontend Interaction:** You fill out the "Add Officer" form and click the **"Add Officer"** button on the `/officers/search/` page.
*   **Backend File & Part:** `OfficerSearch.py` -> `officer_search(request)` handles the `POST` request where `form_name == 'add_officer'`.
*   **Raw SQL Executed:**
    ```sql
    INSERT INTO officers_officer (name, rank, badge_number, team_id) 
    VALUES (%s, %s, %s, %s);
    ```

### 2. Assign officers to teams
*   **Frontend Interaction:** In the "Add Team" form, you type a team name and click **"Add Team"**. Later, when adding an officer, you select that team from the "Assign Team" dropdown.
*   **Backend File & Part:** `OfficerSearch.py` -> `officer_search(request)` handles the `POST` request where `form_name == 'add_team'`.
*   **Raw SQL Executed:**
    ```sql
    INSERT INTO officers_team (team_name) VALUES (%s);
    ```

### 3. Record which officer worked on which day
*   **Frontend Interaction:** You fill out the shift details and click **"Log Shift"** on the `/officers/shifts/` page.
*   **Backend File & Part:** `ShiftTracking.py` -> `shift_tracking(request)` handles the `POST` request.
*   **Raw SQL Executed:**
    ```sql
    INSERT INTO officers_shift (officer_id, work_date, hours) 
    VALUES (%s, %s, %s);
    ```

### 4. Have a login only for admins
*   **Frontend Interaction:** You enter your username and password, then click **"Login"** on the `/login/` page.
*   **Backend File & Part:** `login.py` -> `admin_login(request)` handles the `POST` request to verify credentials.
*   **Raw SQL Executed:**
    ```sql
    SELECT * FROM admin_auth_adminuser WHERE username = %s;
    ```

### 5. Quickly search for officers by their rank or team
*   **Frontend Interaction:** You select options from the "Rank Selection" or "Unit / Division" dropdowns and click **"Initiate Query"**.
*   **Backend File & Part:** `OfficerSearch.py` -> `officer_search(request)` handles the `GET` request and dynamically builds the query based on parameters.
*   **Raw SQL Executed:**
    ```sql
    SELECT o.officer_id, o.name, o.rank, o.badge_number, t.team_name
    FROM officers_officer o
    LEFT JOIN officers_team t ON o.team_id = t.team_id
    WHERE o.rank = %s AND o.team_id = %s;
    ```

### 6. Save information about criminals
*   **Frontend Interaction:** You fill out the "Register New Subject" form and click **"Add Criminal"** on the `/criminals/` page.
*   **Backend File & Part:** `CriminalList.py` -> `criminal_list(request)` handles the `POST` request.
*   **Raw SQL Executed:**
    ```sql
    INSERT INTO criminals_criminal (name, age, date_of_birth, gender, physical_description, is_repeat_offender) 
    VALUES (%s, %s, %s, %s, %s, False);
    ```

### 7. Save all nicknames/street names one criminal uses
*   **Frontend Interaction:** In a criminal's profile (`/criminals/<id>/`), you type an alias and click **"Add Alias"**.
*   **Backend File & Part:** `CriminalProfile.py` -> `criminal_profile(request, criminal_id)` handles the `POST` request where `form_name == 'add_alias'`.
*   **Raw SQL Executed:**
    ```sql
    INSERT INTO criminals_alias (criminal_id, alias_name) 
    VALUES (%s, %s);
    ```

### 8. Keep victim names and phone numbers connected to each crime
*   **Frontend Interaction:** In a crime's detail page (`/crimes/<id>/`), you type a victim's details and click **"Add Victim"**.
*   **Backend File & Part:** `CrimeDetail.py` -> `crime_detail(request, crime_id)` handles the `POST` request where `form_name == 'add_victim'`.
*   **Raw SQL Executed:**
    ```sql
    INSERT INTO crimes_victim (name) VALUES (%s);
    
    -- Links the newly created victim to the crime:
    INSERT INTO crimes_crimevictim (crime_id, victim_id) VALUES (%s, %s);
    ```

### 9. Track arrest warrants (active or cancelled)
*   **Frontend Interaction:** You filter by status or click **"Cancel Warrant"** on the `/warrants/` page.
*   **Backend File & Part:** `WarrantTracking.py` -> `warrant_tracking(request)` handles the `POST` request to change a warrant's status.
*   **Raw SQL Executed:**
    ```sql
    UPDATE warrants_warrant SET status = 'Cancelled' WHERE warrant_id = %s;
    ```

### 10. Write notes about when a criminal was questioned
*   **Frontend Interaction:** In a criminal's profile, you type an interrogation note and click **"Log Interrogation"**.
*   **Backend File & Part:** `CriminalProfile.py` -> `criminal_profile(request, criminal_id)` handles the `POST` request where `form_name == 'add_interrogation'`.
*   **Raw SQL Executed:**
    ```sql
    INSERT INTO criminals_interrogation (criminal_id, interrogation_date, notes) 
    VALUES (%s, %s, %s);
    ```

### 11. Make a "Be On the Lookout" list
*   **Frontend Interaction:** You click **"Active BOLOs"** in the sidebar.
*   **Backend File & Part:** `BOLOList.py` -> `bolo_list(request)` handles the `GET` request when the page loads.
*   **Raw SQL Executed:**
    ```sql
    SELECT w.warrant_id, w.issue_date, c.criminal_id, c.name, c.age, c.gender, c.physical_description
    FROM warrants_warrant w
    JOIN criminals_criminal c ON w.criminal_id = c.criminal_id
    WHERE w.status = 'Active'
    ORDER BY w.issue_date DESC;
    ```

### 12. Record each crime (what happened, when, where)
*   **Frontend Interaction:** You fill out the incident details and click **"Add Crime Record"** on the `/crimes/` page.
*   **Backend File & Part:** `CrimeList.py` -> `crime_list(request)` handles the `POST` request.
*   **Raw SQL Executed:**
    ```sql
    INSERT INTO crimes_crime (description, method_used, location, city, date_time, status) 
    VALUES (%s, %s, %s, %s, %s, %s);
    ```

### 13. List evidence collected and connect it
*   **Frontend Interaction:** In a crime's detail page, you type evidence details and click **"Add Evidence"**.
*   **Backend File & Part:** `CrimeDetail.py` -> `crime_detail(request, crime_id)` handles the `POST` request where `form_name == 'add_evidence'`.
*   **Raw SQL Executed:**
    ```sql
    INSERT INTO crimes_evidence (crime_id, type, description) 
    VALUES (%s, %s, %s);
    ```

### 14. Keep track of court dates and judge names
*   **Frontend Interaction:** You select a Case, enter a Date and Judge, and click **"Add Court Session"** on the `/court/` page.
*   **Backend File & Part:** `CourtCalendar.py` -> `court_list(request)` handles the `POST` request.
*   **Raw SQL Executed:**
    ```sql
    INSERT INTO court_court (case_id, court_date, judge_name) 
    VALUES (%s, %s, %s);
    ```

### 15. Mark cases as "Still open" or "Finished"
*   **Frontend Interaction:** You use the "Status" dropdown while linking a Crime to a Case Record and click **"Create Case"**.
*   **Backend File & Part:** `CaseRecords.py` -> `case_status_list(request)` handles the `POST` request.
*   **Raw SQL Executed:**
    ```sql
    INSERT INTO cases_case (crime_id, status, opened_date) 
    VALUES (%s, %s, %s);
    ```

### 16. Crime Pattern Finder
*   **Frontend Interaction:** You type a trick/method and click **"Analyze Patterns"** on the `/crimes/pattern-finder/` page.
*   **Backend File & Part:** `CrimePatternFinder.py` -> `pattern_finder(request)` handles the `GET` request.
*   **Raw SQL Executed:**
    ```sql
    SELECT crime_id, description, method_used, location, date_time, status
    FROM crimes_crime
    WHERE method_used LIKE %s
    ORDER BY method_used, date_time DESC;
    ```

### 17. Repeat Offender Alert
*   **Frontend Interaction:** You click **"Repeat Offenders"** in the sidebar to load the page.
*   **Backend File & Part:** `RepeatOffenders.py` -> `repeat_offenders(request)` handles the `GET` request when the page loads.
*   **Raw SQL Executed:**
    ```sql
    SELECT c.criminal_id, c.name, COUNT(ci.crime_id) AS crime_count
    FROM criminals_criminal c
    JOIN crimes_crimeinvolvement ci ON c.criminal_id = ci.criminal_id
    GROUP BY c.criminal_id, c.name
    HAVING COUNT(ci.crime_id) >= 2
    ORDER BY crime_count DESC;
    ```
