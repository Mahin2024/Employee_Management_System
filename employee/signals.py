from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Attendance


@receiver(post_save, sender=Attendance) 
def create_alert(sender, instance, created, **kwargs):
    if created and instance.location == 'WFH':
        employee = instance.employee
        email_id=employee.team_leader.email
        print(email_id)
        send_mail(
        subject=f'Regarding WFH employee today {instance.date} ',
        message=f'Your employee {employee} has login Work From Home today',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list= [email_id],
        fail_silently=False,
        )

