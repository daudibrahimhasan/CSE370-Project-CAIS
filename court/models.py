from django.db import models
from cases.models import Case

class Court(models.Model):
    VERDICT_GUILTY = "GUILTY"
    VERDICT_NOT_GUILTY = "NOT_GUILTY"
    VERDICT_DISMISSED = "DISMISSED"
    VERDICT_PLEA = "PLEA_DEAL"
    VERDICT_PENDING = "PENDING"
    VERDICT_CHOICES = [
        (VERDICT_GUILTY, "Guilty"),
        (VERDICT_NOT_GUILTY, "Not Guilty"),
        (VERDICT_DISMISSED, "Dismissed"),
        (VERDICT_PLEA, "Plea Deal"),
        (VERDICT_PENDING, "Pending"),
    ]

    SENTENCE_PRISON = "PRISON"
    SENTENCE_PROBATION = "PROBATION"
    SENTENCE_FINE = "FINE"
    SENTENCE_COMMUNITY = "COMMUNITY_SERVICE"
    SENTENCE_NONE = "NONE"
    SENTENCE_CHOICES = [
        (SENTENCE_PRISON, "Prison"),
        (SENTENCE_PROBATION, "Probation"),
        (SENTENCE_FINE, "Fine"),
        (SENTENCE_COMMUNITY, "Community Service"),
        (SENTENCE_NONE, "None"),
    ]

    court_id = models.AutoField(primary_key=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='court_dates')
    court_date = models.DateField()
    judge_name = models.CharField(max_length=150)
    verdict = models.CharField(max_length=20, choices=VERDICT_CHOICES, default=VERDICT_PENDING)
    verdict_date = models.DateTimeField(null=True, blank=True)
    sentence_type = models.CharField(max_length=30, choices=SENTENCE_CHOICES, null=True, blank=True)
    sentence_length_months = models.IntegerField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    verdict_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Court ID {self.court_id} on {self.court_date} (Judge {self.judge_name})"
