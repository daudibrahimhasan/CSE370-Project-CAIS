from django.db import models
from officers.models import Officer

class Criminal(models.Model):
    criminal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    age = models.IntegerField()
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50)
    physical_description = models.TextField()
    is_repeat_offender = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Nickname(models.Model):
    nickname_id = models.AutoField(primary_key=True)
    criminal = models.ForeignKey(Criminal, on_delete=models.CASCADE, related_name='nicknames')
    alias = models.CharField(max_length=100)

    def __str__(self):
        return self.alias

class Interrogation(models.Model):
    interrogation_id = models.AutoField(primary_key=True)
    officer = models.ForeignKey(Officer, on_delete=models.SET_NULL, null=True, related_name='interrogations')
    criminal = models.ForeignKey(Criminal, on_delete=models.CASCADE, related_name='interrogations_involved')
    date = models.DateTimeField()
    notes = models.TextField()

    def __str__(self):
        return f"Interrogation: {self.criminal.name} on {self.date}"
