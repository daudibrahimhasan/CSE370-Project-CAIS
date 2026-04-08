from django.contrib import admin
from .models import Crime, Victim, VictimPhone, Evidence, CrimeInvolvement, CrimeVictim, Investigates

admin.site.register(Crime)
admin.site.register(Victim)
admin.site.register(VictimPhone)
admin.site.register(Evidence)
admin.site.register(CrimeInvolvement)
admin.site.register(CrimeVictim)
admin.site.register(Investigates)
