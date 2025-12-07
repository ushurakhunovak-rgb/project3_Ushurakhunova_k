from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('timesheet.urls')),  # '/' теперь ведёт на home_view из timesheet/urls.py
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]