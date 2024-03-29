from django.utils import timezone
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core import validators
from django.utils.translation import gettext_lazy as _
import re


class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=is_staff,
            is_active=True, is_superuser=is_superuser, last_login=now,
            date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)
    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user


class Person(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('username'), max_length=15, unique=True,
        help_text=_('Required. 15 characters or fewer. Letters, numbers and @/./+/-/_ characters'),
        validators=[ validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), _('invalid'))]
    )
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()


    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')
    @property
    def full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class Transaction(models.Model):
    TRASACTIONS_CATEGORY = [
        ('market', 'Market'),
        ('transportation', 'Transportation'),
        ('clothing', 'Clothing'),
        ('bills', 'Bills'),
        ('health_expenses', 'Health expenses'),
        ('savings', 'Savings'),
        ('other', 'Other'),
    ]
    date = models.DateField()
    category = models.CharField(
        max_length=15,
        choices=TRASACTIONS_CATEGORY
    )
    description = models.TextField()
    value = models.DecimalField(max_digits=8, decimal_places=2)
    user = ForeignKey(Person, on_delete=models.CASCADE)
