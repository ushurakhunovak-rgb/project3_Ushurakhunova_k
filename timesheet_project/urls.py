from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found  # опционально, для 404
from django.shortcuts import redirect

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Корень сайта (/) — редирект на главную страницу timesheet
    path('', lambda request: redirect('timesheet_list')),

    # Все пути приложения timesheet под префиксом /timesheet/
    path('timesheet/', include('timesheet.urls')),

    # Встроенная авторизация Django (login, logout, password_change и т.д.)
    path('accounts/', include('django.contrib.auth.urls')),
]