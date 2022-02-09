from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal


import requests
from requests_oauthlib import OAuth1

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialApp

from invitations.utils import get_invitation_model

from .models import RawRateReport, User

social_account_removed = Signal()


@receiver(post_save, sender=RawRateReport)
def new_rate_report_alert(sender, instance, **kwargs):
    if not instance.approved:
        super_users = User.objects.filter(is_superuser=True)
        emails = map(lambda x: x.email, super_users)
        hourly = instance.final_hourly if instance.final_hourly else instance.offered_hourly
        guarantee = instance.final_guarantee if instance.final_guarantee \
            else instance.offered_guarantee
        approval_required = instance.user_created_values or not settings.AUTO_APPROVE_RATE_REPORTS
        send_mail(
            f'{"[Approval required]" if approval_required else "[Auto-approved]"} '
            f'New rate report for '
            f'{instance.job_title_name} on {instance.show_title} '
            f'S{instance.season_number}',
            f'New rate report for {instance.job_title_name} '
            f'on {instance.show_title} S{instance.season_number}: '
            f'${hourly}/hr for {guarantee} hours',
            'alert@crewrates.org',
            emails,
            fail_silently=False
        )


@receiver(social_account_removed)
def send_deauthorization_request(sender, request, socialaccount, socialtoken, **kwargs):
    # Get user's social account uid and their auth token (socialtoken) from the database
    # For Facebook: send a DELETE request to:
    # https://graph.facebook.com/{uid}/permissions?access_token={access_token}
    if socialaccount.provider == 'facebook':
        payload = {
            'access_token': socialtoken.token
        }
        response = requests.delete(f'https://graph.facebook.com/{socialaccount.uid}/permissions',
                                   params=payload)
        # print(response.status_code)
        # print(response.text)
    elif socialaccount.provider == 'google':
        payload = {
            'token': socialtoken.token
        }
        headers = {
            'Content-type': 'application/x-www-form-urlencoded'
        }
        response = requests.post('https://oauth2.googleapis.com/revoke', params=payload,
                                 headers=headers)
        # print(response.status_code)
    elif socialaccount.provider == 'twitter':
        app = SocialApp.objects.get(provider='twitter')
        url = u'https://api.twitter.com/1.1/oauth/invalidate_token'
        header_oauth = OAuth1(app.client_id, app.secret, socialtoken.token, socialtoken.token_secret,
                              signature_type='auth_header')
        params = {
            'access_token': socialtoken.token
        }
        response = requests.post(url, auth=header_oauth, params=params)
        # print(response.status_code)
        # print(response.text)


@receiver(user_signed_up)
def user_signed_up(request, user, **kwargs):
    print("in user_signed_up")
    try:
        invitation = get_invitation_model()
        invite = invitation.objects.get(email=user.email)
        user.first_name = invite.first_name
        user.last_name = invite.last_name
        user.preferred_name = invite.preferred_name
        user.save()

    except invitation.DoesNotExist:
        print("this was not an invited user")
