import os
import django
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cais_project.settings')
django.setup()

from criminals.models import Criminal, Nickname, Interrogation
from crimes.models import Crime, Evidence, CrimeInvolvement, Victim, VictimPhone, CrimeVictim
from officers.models import Officer, Team
from warrants.models import Warrant
from cases.models import Case
from court.models import Court

def sync():
    print("Starting Final Database Sync...")
    
    # Clear existing data to avoid duplicates
    Warrant.objects.all().delete()
    CrimeInvolvement.objects.all().delete()
    Evidence.objects.all().delete()
    Crime.objects.all().delete()
    Criminal.objects.all().delete()
    Team.objects.all().delete()
    Officer.objects.all().delete()
    Case.objects.all().delete()

    # TEAMS
    homicide = Team.objects.create(team_name='Homicide')
    narcotics = Team.objects.create(team_name='Narcotics')
    cyber = Team.objects.create(team_name='Cybercrime')
    traffic = Team.objects.create(team_name='Traffic')
    robbery = Team.objects.create(team_name='Robbery')

    # OFFICERS (Marines)
    sengoku    = Officer.objects.create(name='Sengoku',         rank='Detective',   badge_number='B1001', team=homicide)
    garp       = Officer.objects.create(name='Monkey D. Garp', rank='Sergeant',     badge_number='B1002', team=narcotics)
    aokiji     = Officer.objects.create(name='Aokiji',         rank='Officer',      badge_number='B1003', team=cyber)
    akainu     = Officer.objects.create(name='Sakazuki',       rank='Detective',    badge_number='B1004', team=homicide)
    kizaru     = Officer.objects.create(name='Borsalino',      rank='Lieutenant',   badge_number='B1005', team=narcotics)
    smoker     = Officer.objects.create(name='Smoker',         rank='Officer',      badge_number='B1006', team=traffic)
    fujitora   = Officer.objects.create(name='Issho',          rank='Sergeant',     badge_number='B1007', team=robbery)
    coby       = Officer.objects.create(name='Coby',           rank='Detective',    badge_number='B1008', team=cyber)
    tashigi    = Officer.objects.create(name='Tashigi',        rank='Officer',      badge_number='B1009', team=traffic)
    tsuru      = Officer.objects.create(name='Tsuru',          rank='Lieutenant',   badge_number='B1010', team=homicide)

    # CRIMINALS (Pirates — 50+)
    # --- Yonko & their top commanders (most dangerous, repeat offenders) ---
    whitebeard  = Criminal.objects.create(name='Edward "Whitebeard" Newgate',  age=72, gender='Male',   physical_description='Enormous build, white mustache, bisento scar across chest', is_repeat_offender=True)
    kaido       = Criminal.objects.create(name='Kaido of the Beasts',           age=59, gender='Male',   physical_description='Massive frame, spiked club, dragon tattoo covering left arm', is_repeat_offender=True)
    bigmom      = Criminal.objects.create(name='Charlotte "Big Mom" Linlin',    age=68, gender='Female', physical_description='Enormous build, pink hair, homura earrings, candy cane weapon', is_repeat_offender=True)
    shanks      = Criminal.objects.create(name='Red-Haired Shanks',             age=39, gender='Male',   physical_description='Red hair, missing left arm, three scar marks over left eye', is_repeat_offender=True)
    blackbeard  = Criminal.objects.create(name='Marshall D. "Blackbeard" Teach',age=40, gender='Male',   physical_description='Large build, black beard, multiple missing teeth, dual pistols', is_repeat_offender=True)
    # Whitebeard commanders
    marco       = Criminal.objects.create(name='Marco the Phoenix',             age=43, gender='Male',   physical_description='Blonde hair, blue flames, phoenix tattoo on back', is_repeat_offender=True)
    ace         = Criminal.objects.create(name='Portgas D. Ace',                age=20, gender='Male',   physical_description='Freckles, fire tattoo on back reading "ASCE", cowboy hat', is_repeat_offender=True)
    vista       = Criminal.objects.create(name='Vista',                         age=47, gender='Male',   physical_description='Flower-shaped hat, dual swords, handlebar mustache', is_repeat_offender=False)
    # Kaido's crew (Beast Pirates)
    queen       = Criminal.objects.create(name='Queen the Plague',              age=56, gender='Male',   physical_description='Long hair in bun, cyborg arm, mammoth transformation marks', is_repeat_offender=True)
    king        = Criminal.objects.create(name='King the Wildfire',             age=47, gender='Male',   physical_description='All-black mask and wings, extremely tall, lunarian tribal marks', is_repeat_offender=True)
    jack        = Criminal.objects.create(name='Jack the Drought',              age=35, gender='Male',   physical_description='Pale skin, large tusks, metal jaw implant, blonde braid', is_repeat_offender=True)
    ulti        = Criminal.objects.create(name='Ulti',                          age=22, gender='Female', physical_description='Horned headgear, short blue hair, dinosaur scale tattoo on neck', is_repeat_offender=False)
    # Big Mom pirates
    katakuri    = Criminal.objects.create(name='Charlotte Katakuri',            age=48, gender='Male',   physical_description='Scarred mouth hidden by scarf, tallest of siblings, mochi body', is_repeat_offender=True)
    cracker     = Criminal.objects.create(name='Charlotte Cracker',             age=45, gender='Male',   physical_description='Biscuit-armor exterior, thin frame underneath, rapier sword', is_repeat_offender=True)
    smoothie    = Criminal.objects.create(name='Charlotte Smoothie',            age=35, gender='Female', physical_description='Half-giant build, braided green hair, twin swords', is_repeat_offender=False)
    perospero   = Criminal.objects.create(name='Charlotte Perospero',           age=50, gender='Male',   physical_description='Candy-cane staff, lollipop in mouth, tall lanky frame', is_repeat_offender=False)
    # Blackbeard pirates
    shiryu      = Criminal.objects.create(name='Shiryu of the Rain',            age=41, gender='Male',   physical_description='Rain coat, long sword, glasses, emotionless expression', is_repeat_offender=True)
    augur       = Criminal.objects.create(name='Van Augur the Supersonic',      age=28, gender='Male',   physical_description='Long black cloak, sniper rifle, skeletal face paint', is_repeat_offender=True)
    laffitte    = Criminal.objects.create(name='Laffitte',                      age=34, gender='Male',   physical_description='Top hat, white suit, bird wings on back, walking cane', is_repeat_offender=False)
    # Worst Generation
    luffy       = Criminal.objects.create(name='Monkey D. Luffy',               age=19, gender='Male',   physical_description='Straw hat, red vest, scar under left eye, rubber-like agility', is_repeat_offender=True)
    zoro        = Criminal.objects.create(name='Roronoa Zoro',                   age=21, gender='Male',   physical_description='Green hair, three earrings left ear, three swords, scar over left eye', is_repeat_offender=True)
    law         = Criminal.objects.create(name='Trafalgar D. Water Law',         age=26, gender='Male',   physical_description='Spotted hat, tattoos covering hands and neck, nodachi sword', is_repeat_offender=True)
    kidd        = Criminal.objects.create(name='Eustass "Captain" Kid',          age=23, gender='Male',   physical_description='Red hair, goggles, mechanical left arm, massive build', is_repeat_offender=True)
    killer      = Criminal.objects.create(name='Killer',                         age=23, gender='Male',   physical_description='White mask, blonde hair, dual scythe blades on wrists', is_repeat_offender=True)
    hawkins     = Criminal.objects.create(name='Basil Hawkins',                  age=29, gender='Male',   physical_description='Long blonde hair, voodoo straw doll, tarot card motifs', is_repeat_offender=False)
    apoo        = Criminal.objects.create(name='Scratchmen Apoo',                age=29, gender='Male',   physical_description='Dreadlocks, musical instrument body, skeletal face paint', is_repeat_offender=False)
    urouge      = Criminal.objects.create(name='Urouge the Mad Monk',            age=47, gender='Male',   physical_description='Wings on back, large monk staff, heavyset build, monk robes', is_repeat_offender=False)
    drake       = Criminal.objects.create(name='X Drake',                        age=33, gender='Male',   physical_description='Tall, military coat, anchor saber, dinosaur transformation marks', is_repeat_offender=False)
    # Former Warlords
    mihawk      = Criminal.objects.create(name='Dracule "Hawkeye" Mihawk',       age=43, gender='Male',   physical_description='Hawk-like yellow eyes, black cape, cross-shaped necklace, black blade Yoru', is_repeat_offender=True)
    crocodile   = Criminal.objects.create(name='Sir Crocodile',                  age=46, gender='Male',   physical_description='Hook for right hand, scarred face, long coat, cigar always lit', is_repeat_offender=True)
    doflamingo  = Criminal.objects.create(name='Donquixote Doflamingo',          age=41, gender='Male',   physical_description='Feathered pink coat, sunglasses, long blonde hair, string tattoos', is_repeat_offender=True)
    hancock     = Criminal.objects.create(name='Boa Hancock',                    age=31, gender='Female', physical_description='Extremely tall, black hair to waist, snake earrings, Gorgon symbol on back', is_repeat_offender=False)
    kuma        = Criminal.objects.create(name='Bartholomew Kuma',               age=47, gender='Male',   physical_description='Massive cyborg frame, Bible always in hand, paw-print symbol on palms', is_repeat_offender=True)
    moria       = Criminal.objects.create(name='Gecko Moria',                    age=50, gender='Male',   physical_description='Pale skin, stitched face, enormous pale cross-shaped tattoo, zombie hordes', is_repeat_offender=True)
    jinbe       = Criminal.objects.create(name='Jinbe',                          age=46, gender='Male',   physical_description='Whale shark fishman, blue skin, large build, traditional fishman karate robes', is_repeat_offender=False)
    # Roger Pirates / Roger era
    rayleigh    = Criminal.objects.create(name='Silvers Rayleigh',               age=78, gender='Male',   physical_description='Silver hair, round glasses, scar over right eye, old but powerful build', is_repeat_offender=True)
    scopper     = Criminal.objects.create(name='Scopper Gaban',                  age=54, gender='Male',   physical_description='Axe weapons, scruffy hair, tattoos on both arms', is_repeat_offender=False)
    # Other notable pirates
    nami        = Criminal.objects.create(name='Nami',                           age=20, gender='Female', physical_description='Orange hair, tattoo of pinwheel and mikan on left shoulder, climate baton', is_repeat_offender=True)
    robin       = Criminal.objects.create(name='Nico Robin',                     age=28, gender='Female', physical_description='Black hair, blue eyes, "Poneglyphs" tattoos on arms, devil fruit ability', is_repeat_offender=True)
    usopp       = Criminal.objects.create(name='Usopp',                          age=19, gender='Male',   physical_description='Long nose, curly black hair, goggles, slingshot weapon', is_repeat_offender=False)
    sanji       = Criminal.objects.create(name='Vinsmoke Sanji',                 age=21, gender='Male',   physical_description='Blonde hair covering right eye, black suit, curly eyebrow, leg-based fighter', is_repeat_offender=True)
    nami2       = Criminal.objects.create(name='Charlotte Pudding',              age=16, gender='Female', physical_description='Brown wavy hair, third eye on forehead covered by bangs, candy bullets', is_repeat_offender=False)
    yamato      = Criminal.objects.create(name='Yamato',                         age=28, gender='Female', physical_description='Long white hair, oni horns, traditional Japanese robes, kanabo club', is_repeat_offender=False)
    carrot      = Criminal.objects.create(name='Carrot',                         age=21, gender='Female', physical_description='White rabbit ears, orange eyes, bunny features, electro ability', is_repeat_offender=False)
    nefertari   = Criminal.objects.create(name='Nefertari Vivi',                 age=18, gender='Female', physical_description='Blue hair, princess attire, Alabasta royal symbol tattoo', is_repeat_offender=False)
    buggy       = Criminal.objects.create(name='Buggy the Clown',                age=39, gender='Male',   physical_description='Red nose, blue hair divided by line, clown makeup, detachable body parts', is_repeat_offender=True)
    alvida      = Criminal.objects.create(name='Miss All Sunday',                age=26, gender='Female', physical_description='Green hair, sunglasses, long coat, alias used while with Baroque Works', is_repeat_offender=False)
    arlong      = Criminal.objects.create(name='Arlong',                         age=41, gender='Male',   physical_description='Sawshark fishman, blue skin, massive serrated nose, fishman karate', is_repeat_offender=True)
    caesar      = Criminal.objects.create(name='Caesar Clown',                   age=46, gender='Male',   physical_description='Mad scientist appearance, large head, gas mask, lab coat stained with chemicals', is_repeat_offender=True)
    vergo       = Criminal.objects.create(name='Vergo',                          age=41, gender='Male',   physical_description='Tall, business attire, bamboo staff, food always stuck to face', is_repeat_offender=True)
    monet       = Criminal.objects.create(name='Monet',                          age=25, gender='Female', physical_description='Harpy wings, snow-white feathers, glasses, Doflamingo tattoo on wrist', is_repeat_offender=False)
    trebol      = Criminal.objects.create(name='Trebol',                         age=52, gender='Male',   physical_description='Disgusting mucus-covered body, long cloak, stick weapon, sticky substance trail', is_repeat_offender=True)

    # CRIMES
    c1  = Crime.objects.create(description='Armed robbery at convenience store',        method_used='Armed Robbery',     location='5th Ave & 23rd St',        city='New York',     date_time=datetime.datetime(2024,1,5,21,30),  status='Open')
    c2  = Crime.objects.create(description='Residential break-in and theft',            method_used='Forced Entry',       location='88 Maple Drive',            city='Chicago',      date_time=datetime.datetime(2024,1,8,3,15),   status='Open')
    c3  = Crime.objects.create(description='Drug deal bust near park',                  method_used='Drug Distribution',  location='Central Park North',        city='New York',     date_time=datetime.datetime(2024,1,9,18,0),   status='Closed')
    c4  = Crime.objects.create(description='Carjacking at red light',                   method_used='Armed Robbery',     location='Highway 90 Exit 14',        city='Houston',      date_time=datetime.datetime(2024,1,11,22,45), status='Open')
    c5  = Crime.objects.create(description='Online fraud and identity theft',           method_used='Phishing Scam',     location='Remote/Online',             city='Los Angeles',  date_time=datetime.datetime(2024,1,13,10,0),  status='Open')
    c6  = Crime.objects.create(description='Assault with weapon outside nightclub',     method_used='Armed Assault',     location='12 Club Row',               city='Miami',        date_time=datetime.datetime(2024,1,15,1,0),   status='Closed')
    c7  = Crime.objects.create(description='Warehouse robbery using forced entry',      method_used='Forced Entry',       location='300 Industrial Blvd',       city='Chicago',      date_time=datetime.datetime(2024,1,17,2,30),  status='Open')
    c8  = Crime.objects.create(description='Drug trafficking intercept at airport',     method_used='Drug Distribution',  location='JFK Airport Terminal 4',    city='New York',     date_time=datetime.datetime(2024,1,19,14,0),  status='Open')
    c9  = Crime.objects.create(description='Phishing ring targeting elderly citizens',  method_used='Phishing Scam',     location='Multiple Locations',        city='Phoenix',      date_time=datetime.datetime(2024,1,21,9,0),   status='Open')
    c10 = Crime.objects.create(description='Bank robbery using armed threat',           method_used='Armed Robbery',     location='First National Bank',       city='Dallas',       date_time=datetime.datetime(2024,1,23,11,15), status='Open')

    # INVOLVEMENTS
    CrimeInvolvement.objects.create(criminal=kaido,      crime=c1)
    CrimeInvolvement.objects.create(criminal=kaido,      crime=c4)
    CrimeInvolvement.objects.create(criminal=kaido,      crime=c10)
    CrimeInvolvement.objects.create(criminal=blackbeard, crime=c2)
    CrimeInvolvement.objects.create(criminal=blackbeard, crime=c7)
    CrimeInvolvement.objects.create(criminal=doflamingo, crime=c5)
    CrimeInvolvement.objects.create(criminal=crocodile,  crime=c3)
    CrimeInvolvement.objects.create(criminal=crocodile,  crime=c8)
    CrimeInvolvement.objects.create(criminal=king,       crime=c6)
    CrimeInvolvement.objects.create(criminal=king,       crime=c4)

    # WARRANTS
    Warrant.objects.create(criminal=kaido,      issue_date=datetime.date(2024,1,6),  status='Active')
    Warrant.objects.create(criminal=blackbeard, issue_date=datetime.date(2024,1,9),  status='Active')
    Warrant.objects.create(criminal=crocodile,  issue_date=datetime.date(2024,1,10), status='Active')
    Warrant.objects.create(criminal=king,       issue_date=datetime.date(2024,1,16), status='Active')

    # CASES
    for crime in Crime.objects.all():
        Case.objects.create(crime=crime, status=crime.status, opened_date=crime.date_time.date())

    print(f"Sync Successful: {Criminal.objects.count()} Criminals and {Crime.objects.count()} Crimes synchronized.")

if __name__ == "__main__":
    sync()
