from django.db import models
from criminals.models import Criminal
from officers.models import Officer

class Victim(models.Model):
    victim_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class VictimPhone(models.Model):
    phone_id = models.AutoField(primary_key=True)
    victim = models.ForeignKey(Victim, on_delete=models.CASCADE, related_name='phones')
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.phone_number

class Crime(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('Cold', 'Cold Case')
    ]
    crime_id = models.AutoField(primary_key=True)
    description = models.TextField()
    method_used = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    
    # Bridge tables relationships
    criminals_involved = models.ManyToManyField(Criminal, through='CrimeInvolvement', related_name='crimes_involved')
    victims_involved = models.ManyToManyField(Victim, through='CrimeVictim', related_name='crimes_involved')
    officers_investigating = models.ManyToManyField(Officer, through='Investigates', related_name='crimes_investigated')

    def __str__(self):
        return f"Crime #{self.crime_id} - {self.method_used}"

class Evidence(models.Model):
    evidence_id = models.AutoField(primary_key=True)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE, related_name='evidence_items')
    type = models.CharField(max_length=100) # e.g., gun, phone, laptop
    description = models.TextField()

    def __str__(self):
        return f"{self.type} for Crime #{self.crime.crime_id}"

# Bridge Tables explicit definitions
class CrimeInvolvement(models.Model):
    criminal = models.ForeignKey(Criminal, on_delete=models.CASCADE)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.criminal.name} involvement in Crime #{self.crime.crime_id}"

class CrimeVictim(models.Model):
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
    victim = models.ForeignKey(Victim, on_delete=models.CASCADE)

class Investigates(models.Model):
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE)
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE)
    date_worked = models.DateField()

    def __str__(self):
        return f"{self.officer.name} investigating Crime #{self.crime.crime_id}"
