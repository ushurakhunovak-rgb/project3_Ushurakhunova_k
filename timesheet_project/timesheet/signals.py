# timesheet/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models import Sum
from datetime import timedelta

from .models import Timesheet

@receiver(pre_save, sender=Timesheet)
def notify_overtime(sender, instance, **kwargs):
    if instance.pk is None:
        return

    try:
        old = Timesheet.objects.get(pk=instance.pk)
    except Timesheet.DoesNotExist:
        return

    if old.status != 'approved' and instance.status == 'approved':
        start_week = instance.date - timedelta(days=instance.date.weekday())
        end_week = start_week + timedelta(days=6)

        total_hours = Timesheet.objects.filter(
            employee=instance.employee,
            status='approved',
            date__range=[start_week, end_week]
        ).aggregate(Sum('hours'))['hours__sum'] or 0

        if total_hours > 40:
            user = instance.employee.user
            subject = 'Переработка зафиксирована!'
            message = f"""
Уважаемый(ая) {user.get_full_name() or user.username},

За неделю {start_week.strftime('%d.%m.%Y')} — {end_week.strftime('%d.%m.%Y')}
у вас зафиксировано {total_hours} часов (норма 40 ч).

Переработка: {total_hours - 40} ч.

С уважением,
Система Timesheet
            """

            send_mail(
                subject=subject,
                message=message,
                from_email='timesheet@company.com',
                recipient_list=[user.email] if user.email else ['test@example.com'],
                fail_silently=False,
            )