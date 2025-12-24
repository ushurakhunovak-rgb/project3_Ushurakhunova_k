from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum

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


# Проверка на менеджера (superuser или группа Managers)
def is_manager(user):
    return user.is_superuser or user.groups.filter(name='Managers').exists()


class TimesheetListView(LoginRequiredMixin, ListView):
    model = Timesheet
    template_name = 'timesheet_list.html'
    context_object_name = 'timesheets'

    def get_queryset(self):
        if is_manager(self.request.user):
            return Timesheet.objects.all().order_by('-date')  # Менеджер видит ВСЕ записи
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
    template_name = 'timesheet_confirm_delete.html'  # рекомендуется создать отдельный шаблон
    success_url = reverse_lazy('timesheet_list')

    def get_queryset(self):
        return Timesheet.objects.filter(employee__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Запись успешно удалена.')
        return super().delete(request, *args, **kwargs)


# Одобрение/отклонение записи — только для менеджера
@user_passes_test(is_manager, login_url='timesheet_list')
def approve_timesheet(request, pk):
    ts = get_object_or_404(Timesheet, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            ts.status = 'approved'
            messages.success(
                request,
                f'Запись от {ts.date.strftime("%d.%m.%Y")} ({ts.task}) успешно одобрена.'
            )
        elif action == 'reject':
            ts.status = 'rejected'
            messages.error(
                request,
                f'Запись от {ts.date.strftime("%d.%m.%Y")} ({ts.task}) отклонена.'
            )
        else:
            messages.warning(request, 'Неизвестное действие.')

        ts.save()
        return redirect('timesheet_list')

    # GET — показываем страницу подтверждения
    return render(request, 'approve_form.html', {'ts': ts})