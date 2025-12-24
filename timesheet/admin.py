from django.contrib import admin
from .models import Employee, Project, Task, Timesheet

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass

@admin.register(Timesheet)
class TimesheetAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'hours', 'status']