erDiagram
    ADMIN_USER {
        int id PK
        varchar username "UNIQUE"
        varchar password
        datetime last_login "NULL"
        bool is_superuser
        varchar first_name
        varchar last_name
        varchar email
        bool is_staff
        bool is_active
        datetime date_joined
        varchar role
    }

    TEAM {
        int team_id PK
        varchar team_name
    }

    OFFICER {
        int officer_id PK
        varchar name
        varchar rank
        varchar badge_number "UNIQUE"
        int team_id "NULL FK"
    }

    SHIFT {
        int shift_id PK
        date date
        decimal hours_worked
        int officer_id FK
    }

    CRIMINAL {
        int criminal_id PK
        varchar name
        int age
        date date_of_birth "NULL"
        varchar gender
        text physical_description
        bool is_repeat_offender
    }

    NICKNAME {
        int nickname_id PK
        varchar alias
        int criminal_id FK
    }

    INTERROGATION {
        int interrogation_id PK
        datetime date
        text notes
        int criminal_id FK
        int officer_id "NULL FK"
    }

    VICTIM {
        int victim_id PK
        varchar name
    }

    VICTIM_PHONE {
        int phone_id PK
        varchar phone_number
        int victim_id FK
    }

    CRIME {
        int crime_id PK
        text description
        varchar method_used
        varchar location
        varchar city "NULL"
        decimal latitude "NULL"
        decimal longitude "NULL"
        datetime date_time
        varchar status
    }

    EVIDENCE {
        int evidence_id PK
        varchar type
        text description
        int crime_id FK
    }

    CASE {
        int case_id PK
        varchar status
        date opened_date "NULL"
        int crime_id FK
    }

    COURT {
        int court_id PK
        date court_date
        varchar judge_name
        int case_id FK
    }

    WARRANT {
        int warrant_id PK
        date issue_date
        varchar status
        int criminal_id FK
    }

    INVESTIGATES {
        int id PK
        date date_worked
        int crime_id FK
        int officer_id FK
    }

    CRIME_INVOLVEMENT {
        int id PK
        int crime_id FK
        int criminal_id FK
    }

    CRIME_VICTIM {
        int id PK
        int crime_id FK
        int victim_id FK
    }

    TEAM ||--o{ OFFICER : has
    OFFICER ||--o{ SHIFT : works
    OFFICER o|--o{ INTERROGATION : conducts

    CRIMINAL ||--o{ NICKNAME : has
    CRIMINAL ||--o{ INTERROGATION : involved
    CRIMINAL ||--o{ WARRANT : has

    VICTIM ||--o{ VICTIM_PHONE : has

    CRIME ||--o{ EVIDENCE : has
    CRIME ||--o{ CASE : produces
    CASE ||--o{ COURT : schedules

    OFFICER ||--o{ INVESTIGATES : works_on
    CRIME ||--o{ INVESTIGATES : investigated_by

    CRIMINAL ||--o{ CRIME_INVOLVEMENT : involved_in
    CRIME ||--o{ CRIME_INVOLVEMENT : has

    VICTIM ||--o{ CRIME_VICTIM : affected_by
    CRIME ||--o{ CRIME_VICTIM : has

