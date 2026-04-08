from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_auth.urls')),
    path('officers/', include('officers.urls')),
    path('criminals/', include('criminals.urls')),
    path('crimes/', include('crimes.urls')),
    path('cases/', include('cases.urls')),
    path('warrants/', include('warrants.urls')),
]
