from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


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
    # name = models.CharField(max_length=254, null=True, blank=True)
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


class Company(models.Model):
    name = models.CharField(max_length=128, unique=True)


class JobTitle(models.Model):
    title = models.CharField(max_length=128, unique=True)


class Show(models.Model):
    title = models.CharField(max_length=128)


class Network(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Location(models.Model):
    display_name = models.CharField(max_length=128)
    long_name = models.CharField(max_length=128)
    short_name = models.CharField(max_length=128)
    type = models.CharField(max_length=128)


class Season(models.Model):
    title = models.CharField(max_length = 128)
    show = models.ForeignKey(
        Show,
        on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    # genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    union = models.BooleanField()
    company = models.ManyToManyField(
        Company,
        through='SeasonsCompanies',
        through_fields=('season', 'company'),
        blank=True)
    network = models.ForeignKey(
        Network,
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    # locations = scopes[0] from the POST request
    locations = models.ManyToManyField(
        Location,
        through='SeasonsLocations',
        through_fields=('season', 'location'),
        related_name='locations',
        blank=True)
    scopes = models.ManyToManyField(
        Location,
        through='SeasonsScopes',
        through_fields=('season', 'scope'),
        related_name='scopes',
        blank=True)

    REALITY = 'RE'
    DOCUMENTARY = 'DO'
    GAME = 'GA'
    LIVE = 'LI'
    TALK = 'TA'
    GENRE_CHOICES = [
        (REALITY, 'Reality'),
        (DOCUMENTARY, 'Documentary'),
        (GAME, 'Game'),
        (LIVE, 'Live'),
        (TALK, 'Talk'),
    ]
    genre = models.CharField(
        max_length=2,
        choices=GENRE_CHOICES,
        default=REALITY
    )


class RawRateReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title_id = models.SmallIntegerField()
    job_title_name = models.CharField(max_length=128)
    # On form, set localize=False for hourly field
    hourly = models.DecimalField(
        decimal_places=4,
        max_digits=9)
    guarantee = models.PositiveSmallIntegerField()
    show_id = models.SmallIntegerField()
    show_title = models.CharField(max_length=128)
    season_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)])
    company_id = models.SmallIntegerField(null=True, blank=True)
    company_name = models.CharField(max_length=128, blank=True)
    network_id = models.SmallIntegerField(null=True, blank=True)
    network_name = models.CharField(max_length=128, blank=True)
    locations = models.JSONField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    union = models.BooleanField()


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
    raw_report = models.ForeignKey(
        RawRateReport,
        on_delete=models.SET_NULL,
        null=True)


class SeasonsCompanies(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'rates_seasons_companies'


class SeasonsLocations(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        db_table = 'rates_seasons_locations'


class SeasonsScopes(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    scope = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        db_table = 'rates_seasons_scopes'
