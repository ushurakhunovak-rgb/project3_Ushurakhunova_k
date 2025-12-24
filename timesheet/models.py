from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=10.00)  # Для будущих отчётов по зарплате

    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    employees = models.ManyToManyField(Employee, blank=True)  # Сотрудники на проекте

    def __str__(self):
        return self.name

class Task(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.project.name})"

class Timesheet(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает одобрения'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.user.username} - {self.date} - {self.hours}h"

    @property
    def total_salary(self):
        return self.hours * self.employee.hourly_rate
    