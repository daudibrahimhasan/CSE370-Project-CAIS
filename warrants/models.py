from django.db import models
from criminals.models import Criminal

class Warrant(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Cancelled', 'Cancelled'),
    ]
    warrant_id = models.AutoField(primary_key=True)
    criminal = models.ForeignKey(Criminal, on_delete=models.CASCADE, related_name='warrants')
    issue_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"Warrant #{self.warrant_id} - {self.criminal.name} ({self.status})"
