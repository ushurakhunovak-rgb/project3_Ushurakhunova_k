from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone
from django.utils.dateparse import parse_date
from dateutil.relativedelta import relativedelta

from datetime import datetime
from openpyxl import Workbook
from openpyxl.styles import Font

from .models import Timesheet, Employee
from .forms import TimesheetForm


def home_view(request):
    if request.user.is_authenticated:
        total_timesheets = Timesheet.objects.filter(employee__user=request.user).count()
        total_hours = Timesheet.objects.filter(employee__user=request.user).aggregate(Sum('hours'))['hours__sum'] or 0
        context = {'total_timesheets': total_timesheets, 'total_hours': total_hours}
    else:
        context = {}
    return render(request, 'home.html', context)


# Проверка на менеджера (группа Managers)
def is_manager(user):
    return user.groups.filter(name='Managers').exists()


class TimesheetListView(LoginRequiredMixin, ListView):
    model = Timesheet
    template_name = 'timesheet_list.html'
    context_object_name = 'timesheets'

    def get_queryset(self):
        if is_manager(self.request.user):
            return Timesheet.objects.all().order_by('-date')
        return Timesheet.objects.filter(employee__user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_manager'] = is_manager(self.request.user)
        return context


class TimesheetCreateView(LoginRequiredMixin, CreateView):
    model = Timesheet
    form_class = TimesheetForm
    template_name = 'timesheet_form.html'
    success_url = reverse_lazy('timesheet_list')

    def form_valid(self, form):
        employee, created = Employee.objects.get_or_create(
            user=self.request.user,
            defaults={'hourly_rate': 10.00}
        )
        form.instance.employee = employee
        messages.success(self.request, 'Запись успешно добавлена.')
        return super().form_valid(form)


class TimesheetUpdateView(LoginRequiredMixin, UpdateView):
    model = Timesheet
    form_class = TimesheetForm
    template_name = 'timesheet_form.html'
    success_url = reverse_lazy('timesheet_list')

    def get_queryset(self):
        return Timesheet.objects.filter(employee__user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Запись успешно обновлена.')
        return super().form_valid(form)


class TimesheetDeleteView(LoginRequiredMixin, DeleteView):
    model = Timesheet
    template_name = 'timesheet_confirm_delete.html'
    success_url = reverse_lazy('timesheet_list')

    def get_queryset(self):
        return Timesheet.objects.filter(employee__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена.')
        return super().delete(request, *args, **kwargs)


@user_passes_test(is_manager, login_url='timesheet_list')
def approve_timesheet(request, pk):
    ts = get_object_or_404(Timesheet, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            ts.status = 'approved'
            messages.success(request, f'Запись от {ts.date.strftime("%d.%m.%Y")} ({ts.task}) одобрена.')
        elif action == 'reject':
            ts.status = 'rejected'
            messages.error(request, f'Запись от {ts.date.strftime("%d.%m.%Y")} ({ts.task}) отклонена.')
        else:
            messages.warning(request, 'Неизвестное действие.')
        ts.save()
        return redirect('timesheet_list')

    return render(request, 'approve_form.html', {'ts': ts})


# Отчёт по месяцам (для всех — свои, для менеджера — всех)
def report_view(request):
    month_str = request.GET.get('month', timezone.now().strftime('%Y-%m'))
    selected_date = parse_date(f"{month_str}-01") or timezone.now().replace(day=1)
    
    start_date = selected_date
    end_date = selected_date + relativedelta(months=1) - relativedelta(days=1)

    queryset = Timesheet.objects.filter(
        status='approved',
        date__range=(start_date, end_date)
    ).select_related('employee__user', 'task__project')

    if not is_manager(request.user):
        queryset = queryset.filter(employee__user=request.user)
    
    total_hours = queryset.aggregate(Sum('hours'))['hours__sum'] or 0
    total_salary = sum(ts.total_salary for ts in queryset)

    context = {
        'timesheets': queryset.order_by('-date'),
        'total_hours': total_hours,
        'total_salary': total_salary,
        'selected_month': month_str,
        'is_manager': is_manager(request.user),
    }
    return render(request, 'report.html', context)


# Экспорт в Excel — только для менеджера
@user_passes_test(is_manager, login_url='timesheet_list')
def export_timesheets_excel(request):
    month_str = request.GET.get('month')
    if month_str:
        selected_date = parse_date(f"{month_str}-01")
        start_date = selected_date
        end_date = selected_date + relativedelta(months=1) - relativedelta(days=1)
        timesheets = Timesheet.objects.filter(
            status='approved',
            date__range=(start_date, end_date)
        ).select_related('employee__user', 'task__project')
        filename = f"timesheet_{month_str}.xlsx"
    else:
        timesheets = Timesheet.objects.filter(status='approved').select_related('employee__user', 'task__project')
        filename = f"timesheet_full_{datetime.now().strftime('%Y%m%d')}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "Таймшит"

    headers = ['Сотрудник', 'Проект', 'Задача', 'Дата', 'Часы', 'Ставка', 'Зарплата']
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True)

    total_salary = 0
    for ts in timesheets:
        salary = ts.total_salary
        total_salary += salary
        ws.append([
            ts.employee.user.get_full_name() or ts.employee.user.username,
            ts.task.project.name,
            ts.task.name,
            ts.date.strftime("%d.%m.%Y"),
            float(ts.hours),
            float(ts.employee.hourly_rate),
            float(salary),
        ])

    ws.append([])
    ws.append(['ИТОГО ЗАРПЛАТА:', '', '', '', '', '', total_salary])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    wb.save(response)
    return response

from django.core.mail import EmailMessage

@user_passes_test(is_manager, login_url='timesheet_list')
def send_report_email(request):
    # Получаем данные как в salary_report или report_view
    # Используем текущий месяц или все одобренные
    timesheets = Timesheet.objects.filter(status='approved').select_related('employee__user', 'task__project')

    # Собираем текст отчёта
    report_lines = [
        "ОТЧЁТ ПО РАБОЧИМ ЧАСАМ И ЗАРПЛАТЕ",
        "=" * 50,
        ""
    ]

    total_hours_all = 0
    total_salary_all = 0

    current_employee = None
    for ts in timesheets.order_by('employee__user__username', '-date'):
        if current_employee != ts.employee:
            if current_employee is not None:
                report_lines.append("")
            current_employee = ts.employee
            employee_name = ts.employee.user.get_full_name() or ts.employee.user.username
            report_lines.append(f"Сотрудник: {employee_name}")
            report_lines.append(f"Ставка: {ts.employee.hourly_rate} ₽/ч")
            report_lines.append("-" * 40)

        salary = ts.total_salary
        total_hours_all += float(ts.hours)
        total_salary_all += float(salary)

        report_lines.append(
            f"{ts.date.strftime('%d.%m.%Y')} | {ts.task.project.name} → {ts.task.name} | {ts.hours} ч | {salary} ₽"
        )

    report_lines.extend([
        "",
        "=" * 50,
        f"ИТОГО ЧАСОВ: {total_hours_all}",
        f"ИТОГО ЗАРПЛАТА: {total_salary_all} ₽",
        "",
        f"Отчёт сформирован {datetime.now().strftime('%d.%m.%Y в %H:%M')}",
    ])

    report_text = "\n".join(report_lines)

    # Отправляем письмо
    email = EmailMessage(
        subject='Отчёт по таймшиту',
        body=report_text,
        from_email=None,  # использует DEFAULT_FROM_EMAIL
        to=[request.user.email],  # на email менеджера
        reply_to=[request.user.email],
    )

    email.send()

    messages.success(request, 'Отчёт успешно отправлен на вашу почту!')
    return redirect('timesheet_list')