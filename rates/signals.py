from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import RawRateReport, User
from django.core.mail import send_mail

import requests

social_account_removed = Signal()


@receiver(post_save, sender=RawRateReport)
def new_rate_report_alert(sender, instance, **kwargs):
    if not instance.approved:
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


@receiver(social_account_removed)
def send_deauthorization_request(sender, request, socialaccount, token, **kwargs):
    # Get user's social account uid and their auth token (socialtoken) from the database
        # For Facebook: send a DELETE request to:
        # https://graph.facebook.com/{uid}/permissions?access_token={access_token}
    payload = {
        'access_token': token
    }
    response = requests.delete(f'https://graph.facebook.com/{socialaccount.uid}/permissions',
                               params=payload)
    print(response.text)
    pass
