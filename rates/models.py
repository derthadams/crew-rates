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

    def _create_user(self, email, password, is_staff, is_superuser,
                     **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,
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

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % self.pk

    def __str__(self):
        return self.email


class Company(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name = 'company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name


class JobTitle(models.Model):
    title = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.title


class Show(models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Network(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    display_name = models.CharField(max_length=128)
    long_name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)

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

    NON_UNION = "NO"
    IATSE = "IA"
    NABET = "NA"

    UNION_CHOICES = [
        (NON_UNION, 'Non-Union'),
        (IATSE, 'IATSE'),
        (NABET, 'NABET'),
    ]

    DEFAULT_UNION = NON_UNION

    union = models.CharField(
        max_length=2,
        choices=UNION_CHOICES,
        default=DEFAULT_UNION
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

    DEFAULT_GENRE = REALITY

    genre = models.CharField(
        max_length=2,
        choices=GENRE_CHOICES,
        default=DEFAULT_GENRE
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.title = f'{self.show.title} (Season {str(self.number)})'
        super().save(*args, **kwargs)


class RawRateReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.SmallIntegerField()
    job_title_name = models.CharField(max_length=128)
    # TODO: On form, set localize=False for hourly field
    hourly = models.DecimalField(
        decimal_places=4,
        max_digits=9)
    guarantee = models.SmallIntegerField(
        # validators=[MinValueValidator(1)]
    )
    show = models.SmallIntegerField()
    show_title = models.CharField(max_length=128)
    season_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    # company_id = models.SmallIntegerField(null=True, blank=True)
    # company_name = models.CharField(max_length=128, blank=True)
    companies = models.JSONField(null=True, blank=True)
    network = models.SmallIntegerField(null=True, blank=True)
    network_name = models.CharField(max_length=128, blank=True)
    locations = models.JSONField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    union = models.CharField(
        max_length=2,
        choices=Season.UNION_CHOICES,
        default=Season.DEFAULT_UNION
    )
    approved = models.BooleanField(default=False)
    genre = models.CharField(
        max_length=2,
        choices=Season.GENRE_CHOICES,
        default=Season.DEFAULT_GENRE
    )

    def __str__(self):
        return f'{self.user}: {self.show_title} S{self.season_number}, ' \
            f'{self.job_title_name}, ${self.hourly}'


class RateReport(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True)
    job_title = models.ForeignKey(
        JobTitle,
        on_delete=models.SET_NULL,
        null=True)
    hourly = models.DecimalField(
        decimal_places=4,
        max_digits=9)
    guarantee = models.PositiveSmallIntegerField()
    season = models.ForeignKey(
        Season,
        on_delete=models.SET_NULL,
        null=True)
    union = models.CharField(
        max_length=2,
        choices=Season.UNION_CHOICES,
        default=Season.DEFAULT_UNION
    )
    raw_report = models.ForeignKey(
        RawRateReport,
        on_delete=models.SET_NULL,
        null=True)

    def __str__(self):
        return f'{self.user}: {self.season}, {self.job_title}, ${self.hourly}'


class RatesInvitation(Invitation):
    name = models.CharField(
        max_length=128
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
            'name': self.name,
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