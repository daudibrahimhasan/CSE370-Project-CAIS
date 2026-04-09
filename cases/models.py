from django.db import models
from crimes.models import Crime

class Case(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Finished', 'Finished'),
    ]
    case_id = models.AutoField(primary_key=True)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE, related_name='cases')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    opened_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Case #{self.case_id} (Crime #{self.crime.crime_id}) - {self.status}"
