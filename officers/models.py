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

# Note: Investigates will be implemented when Crime model is ready, likely in crimes app to avoid circular imports or using string references.
