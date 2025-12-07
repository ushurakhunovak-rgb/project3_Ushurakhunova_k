from django.shortcuts import render, redirect  # Добавь render и redirect (если нет)
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum  # Добавь Sum, если нет (для статистики)
from .models import Timesheet, Employee
from .forms import TimesheetForm

class TimesheetListView(LoginRequiredMixin, ListView):
    model = Timesheet
    template_name = 'timesheet_list.html'
    context_object_name = 'timesheets'

    def get_queryset(self):
        # Только свои записи (безопасность)
        return Timesheet.objects.filter(employee__user=self.request.user).order_by('-date')

class TimesheetCreateView(LoginRequiredMixin, CreateView):
    model = Timesheet
    form_class = TimesheetForm
    template_name = 'timesheet_form.html'
    success_url = reverse_lazy('timesheet_list')

    def form_valid(self, form):
        form.instance.employee = Employee.objects.get(user=self.request.user)  # Связь с текущим
        return super().form_valid(form)

class TimesheetUpdateView(LoginRequiredMixin, UpdateView):
    model = Timesheet
    form_class = TimesheetForm
    template_name = 'timesheet_form.html'
    success_url = reverse_lazy('timesheet_list')

    def get_queryset(self):
        # Только свои
        return Timesheet.objects.filter(employee__user=self.request.user)

class TimesheetDeleteView(LoginRequiredMixin, DeleteView):
    model = Timesheet
    success_url = reverse_lazy('timesheet_list')

    def get_queryset(self):
        # Только свои
        return Timesheet.objects.filter(employee__user=self.request.user)
    
    from django.shortcuts import render
from django.db.models import Sum
from .models import Timesheet

def home_view(request):
    if request.user.is_authenticated:
        total_timesheets = Timesheet.objects.filter(employee__user=request.user).count()
        total_hours = Timesheet.objects.filter(employee__user=request.user).aggregate(Sum('hours'))['hours__sum'] or 0
        context = {'total_timesheets': total_timesheets, 'total_hours': total_hours}
    else:
        context = {}
    return render(request, 'home.html', context)