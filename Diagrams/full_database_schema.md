erDiagram
    admin_auth_adminuser {
        int id PK
        varchar password
        datetime last_login "NULL"
        bool is_superuser
        varchar username "UNIQUE"
        varchar first_name
        varchar last_name
        varchar email
        bool is_staff
        bool is_active
        datetime date_joined
        varchar role
    }

    admin_auth_adminuser_groups {
        int id PK
        bigint adminuser_id FK "UNIQUE WITH group_id"
        int group_id FK "UNIQUE WITH adminuser_id"
    }

    admin_auth_adminuser_user_permissions {
        int id PK
        bigint adminuser_id FK "UNIQUE WITH permission_id"
        int permission_id FK "UNIQUE WITH adminuser_id"
    }

    auth_group {
        int id PK
        varchar name "UNIQUE"
    }

    auth_group_permissions {
        int id PK
        int group_id FK "UNIQUE WITH permission_id"
        int permission_id FK "UNIQUE WITH group_id"
    }

    auth_permission {
        int id PK
        int content_type_id FK "UNIQUE WITH codename"
        varchar codename "UNIQUE WITH content_type_id"
        varchar name
    }

    django_content_type {
        int id PK
        varchar app_label "UNIQUE WITH model"
        varchar model "UNIQUE WITH app_label"
    }

    django_admin_log {
        int id PK
        text object_id "NULL"
        varchar object_repr
        smallint action_flag
        text change_message
        int content_type_id FK "NULL"
        bigint user_id FK
        datetime action_time
    }

    django_migrations {
        int id PK
        varchar app
        varchar name
        datetime applied
    }

    django_session {
        varchar session_key PK
        text session_data
        datetime expire_date
    }

    officers_team {
        int team_id PK
        varchar team_name
    }

    officers_officer {
        int officer_id PK
        varchar name
        varchar rank
        varchar badge_number "UNIQUE"
        int team_id FK "NULL"
    }

    officers_shift {
        int shift_id PK
        date date
        decimal hours_worked
        int officer_id FK
    }

    criminals_criminal {
        int criminal_id PK
        varchar name
        int age
        varchar gender
        text physical_description
        bool is_repeat_offender
        date date_of_birth "NULL"
    }

    criminals_nickname {
        int nickname_id PK
        varchar alias
        int criminal_id FK
    }

    criminals_interrogation {
        int interrogation_id PK
        datetime date
        text notes
        int criminal_id FK
        int officer_id FK "NULL"
    }

    crimes_victim {
        int victim_id PK
        varchar name
    }

    crimes_victimphone {
        int phone_id PK
        varchar phone_number
        int victim_id FK
    }

    crimes_crime {
        int crime_id PK
        text description
        varchar method_used
        varchar location
        datetime date_time
        varchar status
        varchar city "NULL"
        decimal latitude "NULL"
        decimal longitude "NULL"
    }

    crimes_evidence {
        int evidence_id PK
        varchar type
        text description
        int crime_id FK
    }

    crimes_investigates {
        int id PK
        date date_worked
        int crime_id FK
        int officer_id FK
    }

    crimes_crimeinvolvement {
        int id PK
        int crime_id FK
        int criminal_id FK
    }

    crimes_crimevictim {
        int id PK
        int crime_id FK
        int victim_id FK
    }

    cases_case {
        int case_id PK
        varchar status
        int crime_id FK
        date opened_date "NULL"
    }

    court_court {
        int court_id PK
        date court_date
        varchar judge_name
        int case_id FK
    }

    warrants_warrant {
        int warrant_id PK
        date issue_date
        varchar status
        int criminal_id FK
    }

    admin_auth_adminuser ||--o{ admin_auth_adminuser_groups : has
    auth_group ||--o{ admin_auth_adminuser_groups : includes
    admin_auth_adminuser ||--o{ admin_auth_adminuser_user_permissions : has
    auth_permission ||--o{ admin_auth_adminuser_user_permissions : grants
    auth_group ||--o{ auth_group_permissions : has
    auth_permission ||--o{ auth_group_permissions : grants
    django_content_type ||--o{ auth_permission : scopes
    admin_auth_adminuser ||--o{ django_admin_log : creates
    django_content_type o|--o{ django_admin_log : describes

    officers_team o|--o{ officers_officer : has
    officers_officer ||--o{ officers_shift : works
    officers_officer o|--o{ criminals_interrogation : conducts
    officers_officer ||--o{ crimes_investigates : investigates

    criminals_criminal ||--o{ criminals_nickname : has
    criminals_criminal ||--o{ criminals_interrogation : involved_in
    criminals_criminal ||--o{ warrants_warrant : has
    criminals_criminal ||--o{ crimes_crimeinvolvement : involved_in

    crimes_victim ||--o{ crimes_victimphone : has
    crimes_victim ||--o{ crimes_crimevictim : affected_by

    crimes_crime ||--o{ crimes_evidence : has
    crimes_crime ||--o{ crimes_investigates : assigned_to
    crimes_crime ||--o{ crimes_crimeinvolvement : involves
    crimes_crime ||--o{ crimes_crimevictim : affects
    crimes_crime ||--o{ cases_case : opens

    cases_case ||--o{ court_court : schedules
