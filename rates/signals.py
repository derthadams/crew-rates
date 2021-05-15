from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RawRateReport, User
from django.core.mail import send_mail


@receiver(post_save, sender=RawRateReport)
def new_rate_report_alert(sender, instance, **kwargs):
    super_users = User.objects.filter(is_superuser=True)
    emails = map(lambda x: x.email, super_users)
    send_mail(
        f'[crewrates.org alert] New rate report for '
        f'{instance.job_title_name} on {instance.show_title} '
        f'S{instance.season_number}',
        f'New rate report for {instance.job_title_name} '
        f'on {instance.show_title} S{instance.season_number}: '
        f'${instance.hourly}/hr for {instance.guarantee} hours',
        'alert@crewrates.org',
        emails,
        fail_silently=False
    )
