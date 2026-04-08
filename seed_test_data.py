
import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cais_project.settings')
django.setup()

from officers.models import Team, Officer, Shift
from criminals.models import Criminal, Nickname, Interrogation
from crimes.models import Crime, Victim, VictimPhone, CrimeInvolvement, Evidence, CrimeVictim
from warrants.models import Warrant
from cases.models import Case
from court.models import Court

def seed():
    # 1. Teams & Officers
    narcotics = Team.objects.create(team_name="Narcotics")
    traffic = Team.objects.create(team_name="Traffic")
    
    o1 = Officer.objects.create(name="James Bond", rank="Detective", badge_number="007", team=narcotics)
    o2 = Officer.objects.create(name="Sarah Connor", rank="Sergeant", badge_number="SC101", team=traffic)
    
    Shift.objects.create(officer=o1, date=datetime.date.today(), hours_worked=8)
    Shift.objects.create(officer=o2, date=datetime.date.today(), hours_worked=10)
    
    # 2. Criminals
    c1 = Criminal.objects.create(name="John Doe", age=30, date_of_birth=datetime.date(1994, 1, 1), gender="Male", physical_description="Scar on left eye, snake tattoo on arm")
    c2 = Criminal.objects.create(name="Jane Smith", age=25, date_of_birth=datetime.date(1999, 5, 20), gender="Female", physical_description="Height 5'6, blonde hair")
    
    Nickname.objects.create(criminal=c1, alias="The Snake")
    Nickname.objects.create(criminal=c1, alias="Johnny")
    
    Interrogation.objects.create(officer=o1, criminal=c1, date=datetime.datetime.now(), notes="Subject refused to speak without lawyer.")
    
    # 3. Crimes & Involvement (Triggers Pattern Finder & Repeat Offender)
    crime_method = "Smashed front window with a brick"
    
    crime1 = Crime.objects.create(description="Jewelry store heist", method_used=crime_method, location="Downtown", date_time=datetime.datetime.now(), status="Open")
    crime2 = Crime.objects.create(description="Clothing store robbery", method_used=crime_method, location="Uptown", date_time=datetime.datetime.now() - datetime.timedelta(days=2), status="Open")
    crime3 = Crime.objects.create(description="Random assault", method_used="Physical fight", location="Park", date_time=datetime.datetime.now() - datetime.timedelta(days=5), status="Closed")
    
    # John Doe (c1) involved in crime1 and crime2 -> Repeat Offender!
    CrimeInvolvement.objects.create(criminal=c1, crime=crime1)
    CrimeInvolvement.objects.create(criminal=c1, crime=crime2)
    CrimeInvolvement.objects.create(criminal=c2, crime=crime3)
    
    # 4. Victims
    v1 = Victim.objects.create(name="Alice Wonderland")
    VictimPhone.objects.create(victim=v1, phone_number="01812345678")
    CrimeVictim.objects.create(crime=crime1, victim=v1)
    
    # 5. Evidence
    Evidence.objects.create(crime=crime1, type="Brick", description="Red clay brick found inside the store.")
    Evidence.objects.create(crime=crime2, type="Brick", description="Broken brick fragments.")
    
    # 6. Warrants & BOLO
    Warrant.objects.create(criminal=c1, issue_date=datetime.date.today(), status="Active")
    Warrant.objects.create(criminal=c2, issue_date=datetime.date.today(), status="Cancelled")
    
    # 7. Cases & Court
    case1 = Case.objects.create(crime=crime1, status="Open")
    Court.objects.create(case=case1, court_date=datetime.date.today() + datetime.timedelta(days=30), judge_name="John Marshall")
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
