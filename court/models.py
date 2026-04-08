from django.db import models
from cases.models import Case

class Court(models.Model):
    court_id = models.AutoField(primary_key=True)
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='court_dates')
    court_date = models.DateField()
    judge_name = models.CharField(max_length=150)

    def __str__(self):
        return f"Court ID {self.court_id} on {self.court_date} (Judge {self.judge_name})"
