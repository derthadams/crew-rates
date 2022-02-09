import uuid

from captcha.fields import ReCaptchaField

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.contrib.sites.models import Site
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from invitations import signals
from invitations.models import Invitation
from invitations.adapters import get_invitations_adapter


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, first_name=None, last_name=None, preferred_name=None,
                     **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            preferred_name=preferred_name,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name=None, last_name=None,
                    preferred_name=None, **extra_fields):
        return self._create_user(email, password, False, False, first_name, last_name,
                                 preferred_name,**extra_fields)

    def create_superuser(self, email, password, first_name=None, last_name=None,
                         preferred_name=None, **extra_fields):
        user = self._create_user(email, password, True, True, first_name, last_name,
                                 preferred_name,**extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    preferred_name = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % self.pk

    def __str__(self):
        return self.email


class Company(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class JobTitle(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Show(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Network(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    display_name = models.CharField(max_length=128)
    long_name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name


class Season(models.Model):
    title = models.CharField(max_length=128, blank=True)
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    NON_UNION = "NO"
    IATSE = "IA"
    NABET = "NA"

    UNION_CHOICES = [
        (NON_UNION, 'Non-Union'),
        (IATSE, 'IATSE'),
        (NABET, 'NABET'),
    ]

    # DEFAULT_UNION = NON_UNION

    union = models.CharField(
        max_length=4,
        choices=UNION_CHOICES,
        null=True
    )
    companies = models.ManyToManyField(
        Company,
        blank=True)
    network = models.ForeignKey(
        Network,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    locations = models.ManyToManyField(
        Location,
        related_name='locations',
        blank=True)
    scopes = models.ManyToManyField(
        Location,
        related_name='scopes',
        blank=True)

    REALITY = 'RE'
    DOCUMENTARY = 'DO'
    GAME = 'GA'
    LIVE = 'LI'
    TALK = 'TA'
    JUDGE = 'JU'
    OTHER_UNSCRIPTED = 'OT'
    SCRIPTED = 'SC'

    GENRE_CHOICES = [
        (REALITY, 'Reality'),
        (DOCUMENTARY, 'Documentary'),
        (GAME, 'Game Show'),
        (LIVE, 'Live Show'),
        (TALK, 'Talk Show'),
        (JUDGE, 'Judge Show'),
        (OTHER_UNSCRIPTED, 'Other Unscripted'),
        (SCRIPTED, 'Scripted'),

    ]

    # DEFAULT_GENRE = REALITY

    genre = models.CharField(
        max_length=4,
        choices=GENRE_CHOICES,
        null=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # self.title = f'{self.show.title} (Season {str(self.number)})'
        self.title = self.show.title # noqa
        super().save(*args, **kwargs)


class RawRateReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show = models.CharField(max_length=36)
    show_title = models.CharField(max_length=128)
    show_matches = models.ManyToManyField(
        Show,
        related_name='show_matches',
        null=True)
    season_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    companies = models.JSONField(null=True, blank=True)
    company_matches = models.ManyToManyField(
        Company,
        related_name='company_matches',
        null=True)
    network = models.CharField(max_length=36, null=True, blank=True)
    network_name = models.CharField(max_length=128, null=True, blank=True)
    network_matches = models.ManyToManyField(
        Network,
        related_name='network_matches',
        null=True)
    genre = models.CharField(
        max_length=4,
        choices=Season.GENRE_CHOICES,
        null=True,
        blank=True
    )
    union = models.CharField(
        max_length=4,
        choices=Season.UNION_CHOICES,
        null=True,
        blank=True
    )
    locations = models.JSONField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    job_title = models.CharField(max_length=36)
    job_title_name = models.CharField(max_length=128)
    job_title_matches = models.ManyToManyField(
        JobTitle,
        related_name='job_title_matches',
        null=True)
    offered_hourly = models.DecimalField(
        decimal_places=4,
        max_digits=9)
    offered_guarantee = models.PositiveSmallIntegerField()
    negotiated = models.BooleanField()
    increased = models.BooleanField(null=True, blank=True)
    final_hourly = models.DecimalField(
        decimal_places=4,
        max_digits=9,
        null=True,
        blank=True
    )
    final_guarantee = models.PositiveSmallIntegerField(null=True, blank=True)

    approved = models.BooleanField(default=False)
    user_created_values = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        hourly = self.final_hourly if self.final_hourly else self.offered_hourly
        return f'{self.user}: {self.show_title} S{self.season_number}, ' \
            f'{self.job_title_name}, ${hourly}'


class RateReport(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True)
    season = models.ForeignKey(
        Season,
        on_delete=models.SET_NULL,
        null=True)
    union = models.CharField(
        max_length=4,
        choices=Season.UNION_CHOICES,
        null=True
    )
    job_title = models.ForeignKey(
        JobTitle,
        on_delete=models.SET_NULL,
        null=True
    )
    offered_hourly = models.DecimalField(
        decimal_places=4,
        max_digits=9)
    offered_guarantee = models.PositiveSmallIntegerField()
    negotiated = models.BooleanField()
    increased = models.BooleanField(null=True)
    final_hourly = models.DecimalField(
        decimal_places=4,
        max_digits=9,
        null=True)
    final_guarantee = models.PositiveSmallIntegerField(null=True)

    raw_report = models.ForeignKey(
        RawRateReport,
        on_delete=models.SET_NULL,
        null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        hourly = self.final_hourly if self.final_hourly else self.offered_hourly
        return f'{self.user}: {self.season}, {self.job_title}, ${hourly}'


class RatesInvitation(Invitation):
    first_name = models.CharField(
        max_length=128
    )
    last_name = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )
    preferred_name = models.CharField(
        max_length=128,
        null=True,
        blank=True
    )

    def send_invitation(self, request, **kwargs):
        current_site = kwargs.pop('site', Site.objects.get_current())
        invite_url = reverse('invitations:accept-invite',
                             args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)
        ctx = kwargs
        ctx.update({
            'invite_url': invite_url,
            'site_name': current_site.name,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'preferred_name': self.preferred_name,
            'email': self.email,
            'key': self.key,
            'inviter': self.inviter,
        })

        email_template = 'invitations/email/email_invite'

        get_invitations_adapter().send_mail(
            email_template,
            self.email,
            ctx)
        self.sent = timezone.now()
        self.save()

        signals.invite_url_sent.send(
            sender=self.__class__,
            instance=self,
            invite_url_sent=invite_url,
            inviter=self.inviter)


class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=512)
    message = models.TextField()
    captcha = ReCaptchaField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
