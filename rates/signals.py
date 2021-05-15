from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RawRateReport, User
from django.core.mail import send_mail


@receiver(post_save, sender=RawRateReport)
def new_rate_report_alert(sender, instance, **kwargs):
    super_users = User.objects.filter(is_superuser=True)
    emails = map(lambda x: x.email, super_users)
    send_mail(
        '[crewrates.org alert] New rate report',
        f'New rate report for {instance.job_title_name} on {instance.show_title} '
        f'S{instance.season_number}',
        'alert@crewrates.org',
        emails,
        fail_silently=False
    )
