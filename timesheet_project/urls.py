from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse  # Добавь этот импорт

urlpatterns = [
    path('', lambda request: HttpResponse('Добро пожаловать в Timesheet! <a href="/admin/">Админка</a> | <a href="/timesheet/">Timesheets</a> | <a href="/accounts/login/">Войти</a>')),  # Корневой путь
    path('admin/', admin.site.urls),
    path('timesheet/', include('timesheet.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]