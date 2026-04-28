from django.db import models

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=100)

    def __str__(self):
        return self.team_name

class Officer(models.Model):
    officer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    rank = models.CharField(max_length=100)
    badge_number = models.CharField(max_length=50, unique=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='officers')

    def __str__(self):
        return f"{self.rank} {self.name} ({self.badge_number})"

class Shift(models.Model):
    shift_id = models.AutoField(primary_key=True)
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE, related_name='shifts')
    date = models.DateField()
    hours_worked = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.officer.name} - {self.date}"

class Assignment(models.Model):
    TASK_INVESTIGATE_CRIME = "INVESTIGATE_CRIME"
    TASK_SURVEILLANCE_CRIMINAL = "SURVEILLANCE_CRIMINAL"
    TASK_ARREST = "ARREST"
    TASK_COURT_APPEARANCE = "COURT_APPEARANCE"
    TASK_EVIDENCE_HANDLING = "EVIDENCE_HANDLING"
    TASK_OTHER = "OTHER"
    TASK_CHOICES = [
        (TASK_INVESTIGATE_CRIME, "Investigate Crime"),
        (TASK_SURVEILLANCE_CRIMINAL, "Surveillance (Criminal)"),
        (TASK_ARREST, "Arrest"),
        (TASK_COURT_APPEARANCE, "Court Appearance"),
        (TASK_EVIDENCE_HANDLING, "Evidence Handling"),
        (TASK_OTHER, "Other"),
    ]

    STATUS_ASSIGNED = "ASSIGNED"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_CHOICES = [
        (STATUS_ASSIGNED, "Assigned"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    assignment_id = models.AutoField(primary_key=True)
    officer = models.ForeignKey("officers.Officer", on_delete=models.CASCADE, related_name="assignments")
    task_type = models.CharField(max_length=50, choices=TASK_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ASSIGNED)
    priority = models.IntegerField(default=3)
    sector_name = models.CharField(max_length=100, null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    crime = models.ForeignKey("crimes.Crime", null=True, blank=True, on_delete=models.SET_NULL, related_name="assignments")
    criminal = models.ForeignKey("criminals.Criminal", null=True, blank=True, on_delete=models.SET_NULL, related_name="assignments")
    case = models.ForeignKey("cases.Case", null=True, blank=True, on_delete=models.SET_NULL, related_name="assignments")
    warrant = models.ForeignKey("warrants.Warrant", null=True, blank=True, on_delete=models.SET_NULL, related_name="assignments")

    def __str__(self):
        return f"{self.officer} - {self.task_type} ({self.status})"
