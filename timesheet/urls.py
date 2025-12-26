from django.urls import path
from .views import (
    TimesheetListView,
    TimesheetCreateView,
    TimesheetUpdateView,
    TimesheetDeleteView,
    approve_timesheet,
    report_view,
    export_timesheets_excel,
    send_report_email,
)

urlpatterns = [
    # Главная страница приложения — сразу список всех записей
    # URL: /timesheet/
    path('', TimesheetListView.as_view(), name='timesheet_list'),

    # Создание новой записи
    # URL: /timesheet/create/
    path('create/', TimesheetCreateView.as_view(), name='timesheet_create'),

    # Редактирование записи
    # URL: /timesheet/<id>/update/
    path('<int:pk>/update/', TimesheetUpdateView.as_view(), name='timesheet_update'),

    # Удаление записи (с подтверждением)
    # URL: /timesheet/<id>/delete/
    path('<int:pk>/delete/', TimesheetDeleteView.as_view(), name='timesheet_delete'),

    # Страница одобрения/отклонения записи (только для менеджера)
    # URL: /timesheet/<id>/approve/
    path('<int:pk>/approve/', approve_timesheet, name='timesheet_approve'),

    # Отчёт по часам и зарплате (с фильтром по месяцу)
    # URL: /timesheet/report/
    path('report/', report_view, name='report'),

    # Экспорт всех одобренных записей в Excel
    # URL: /timesheet/export/
    path('export/', export_timesheets_excel, name='export_excel'),

    # Отправка отчёта на email (для менеджера)
    # URL: /timesheet/send-email/
    path('send-email/', send_report_email, name='send_report_email'),
]