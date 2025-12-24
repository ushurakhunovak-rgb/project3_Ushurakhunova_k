from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # Импорт redirect

urlpatterns = [
    path('', lambda request: redirect('home')),  # / → /timesheet/ (home_view)
    path('admin/', admin.site.urls),
    path('timesheet/', include('timesheet.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]