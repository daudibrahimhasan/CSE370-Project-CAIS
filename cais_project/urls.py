from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

import BOLOList
import CaseDetail
import CaseRecords
import CourtCalendar
import CourtDetail
import CrimeDetail
import CrimeList
import CrimePatternFinder
import CriminalList
import CriminalProfile
import CriminalRegistry
import OfficerSearch
import RepeatOffenders
import ShiftTracking
import WarrantTracking
import dashboard
import features
import index
import login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.svg', permanent=False)),
    path('', index.home, name='home'),
    path('features/', features.features_page, name='features'),
    path('login/', login.admin_login, name='admin_login'),
    path('logout/', login.admin_logout, name='admin_logout'),
    path('dashboard/', dashboard.dashboard, name='dashboard'),
    path('officers/search/', OfficerSearch.officer_search, name='officer_search'),
    path('officers/shifts/', ShiftTracking.shift_tracking, name='shift_tracking'),
    path('criminals/', CriminalList.criminal_list, name='criminal_list'),
    path('criminals/registry/', CriminalRegistry.criminal_registry, name='criminal_registry'),
    path('criminals/repeat-offenders/', RepeatOffenders.repeat_offenders, name='repeat_offenders'),
    path('criminals/<int:criminal_id>/', CriminalProfile.criminal_profile, name='criminal_profile'),
    path('crimes/', CrimeList.crime_list, name='crime_list'),
    path('crimes/pattern-finder/', CrimePatternFinder.pattern_finder, name='pattern_finder'),
    path('crimes/<int:crime_id>/', CrimeDetail.crime_detail, name='crime_detail'),
    path('warrants/', WarrantTracking.warrant_tracking, name='warrant_tracking'),
    path('warrants/bolo/', BOLOList.bolo_list, name='bolo_list'),
    path('cases/', CaseRecords.case_status_list, name='case_status_list'),
    path('cases/<int:case_id>/', CaseDetail.case_detail, name='case_detail'),
    path('court/', CourtCalendar.court_list, name='court_list'),
    path('court/<int:court_id>/', CourtDetail.court_detail, name='court_detail'),
]
