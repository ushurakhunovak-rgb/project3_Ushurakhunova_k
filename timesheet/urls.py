from django.urls import path
from . import views  # Импорт views (home_view, классы и approve_timesheet)

urlpatterns = [
    path('', views.home_view, name='home'),  # /timesheet/ — твоя красивая главная страница
    path('list/', views.TimesheetListView.as_view(), name='timesheet_list'),  # /timesheet/list/
    path('create/', views.TimesheetCreateView.as_view(), name='timesheet_create'),
    path('<int:pk>/update/', views.TimesheetUpdateView.as_view(), name='timesheet_update'),
    path('<int:pk>/delete/', views.TimesheetDeleteView.as_view(), name='timesheet_delete'),
    
    # Новый URL для одобрения (только менеджер)
    path('<int:pk>/approve/', views.approve_timesheet, name='approve_timesheet'),
]