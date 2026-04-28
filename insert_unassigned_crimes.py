import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cais_project.settings')
django.setup()

from django.db import connection

crimes = [
    ('Purse snatching near subway entrance', 'Phone snatching', 'Times Square Subway Station', 'New York', '2026-04-20 08:30:00', 'Open'),
    ('Armed robbery at late-night deli', 'Armed home invasion', 'Bronx Bodega on Grand Ave', 'New York', '2026-04-19 14:15:00', 'Open'),
    ('Vehicle stolen from hospital parking lot', 'Vehicle theft', 'Mount Sinai Parking Garage', 'New York', '2026-04-18 11:00:00', 'Open'),
    ('Fraudulent wire transfers from elderly account', 'Wire fraud', 'Midtown Financial Office', 'New York', '2026-04-17 22:45:00', 'Open'),
    ('Storefront window smashed, electronics taken', 'Storefront smash-and-grab', 'SoHo Electronics Outlet', 'New York', '2026-04-16 06:20:00', 'Open'),
    ('Credit cards cloned at gas station terminal', 'Card skimming', 'Staten Island Gas Station', 'New York', '2026-04-15 09:00:00', 'Open'),
    ('Narcotics deal observed by undercover', 'Narcotics transaction', 'Washington Heights Corner', 'New York', '2026-04-14 16:30:00', 'Open'),
    ('Forced entry into brownstone residence', 'Forced entry burglary', 'Park Slope Brownstone', 'New York', '2026-04-13 03:10:00', 'Open'),
    ('Counterfeit checks cashed at multiple banks', 'Check fraud', 'Harlem Check Cashing Store', 'New York', '2026-04-12 20:00:00', 'Open'),
    ('Identity documents forged for loan applications', 'Identity theft', 'Queens Boulevard Credit Union', 'New York', '2026-04-11 07:30:00', 'Open'),
    ('Cargo container broken into at port', 'Cargo theft', 'Red Hook Shipping Terminal', 'New York', '2026-04-10 12:45:00', 'Open'),
    ('Pharmacy held at gunpoint', 'Commercial robbery', 'Williamsburg Pharmacy', 'New York', '2026-04-09 23:15:00', 'Open'),
    ('Tourist assaulted and robbed in park', 'Assault and robbery', 'Central Park West Entrance', 'New York', '2026-04-08 10:00:00', 'Open'),
    ('Extortion threats to restaurant owner', 'Extortion', 'Little Italy Restaurant Row', 'New York', '2026-04-07 01:30:00', 'Open'),
    ('Illegal firearm found during traffic stop', 'Firearms possession', 'Cross Bronx Expressway Ramp', 'New York', '2026-04-06 15:00:00', 'Open'),
    ('Fake credit cards used for luxury purchases', 'Credit card fraud', 'Fifth Avenue Department Store', 'New York', '2026-04-05 18:20:00', 'Open'),
    ('Jewelry store robbed at closing time', 'Commercial robbery', 'Diamond District Showroom', 'New York', '2026-04-04 05:45:00', 'Open'),
]

with connection.cursor() as cursor:
    for desc, method, loc, city, dt, status in crimes:
        cursor.execute(
            'INSERT INTO crimes_crime (description, method_used, location, city, latitude, longitude, date_time, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            [desc, method, loc, city, 0, 0, dt, status]
        )
    print(f'Inserted {len(crimes)} unassigned crimes (no suspects identified).')

if __name__ == '__main__':
    pass
