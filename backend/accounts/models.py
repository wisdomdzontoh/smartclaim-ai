from django.contrib.auth.models import AbstractUser
from django.db import models
import pytz

class User(AbstractUser):
    # ——————————— Core Role & Tenant Info ———————————
    ROLE_CHOICES = [
        ('superadmin',    'Super Admin'),
        ('company_admin', 'Company Admin'),
        ('supervisor',    'Supervisor'),
        ('claims_handler','Claims Handler'),
        ('customer',      'Customer'),
    ]
    role       = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    company    = models.ForeignKey(
                   'companies.Company',
                   on_delete=models.SET_NULL,
                   null=True,
                   blank=True,
                   help_text="Which tenant this user belongs to"
                )

    # ——————————— Contact & Profile ———————————
    phone_number    = models.CharField(
                         max_length=30,
                         blank=True,
                         help_text="E.g. +1-555-123-4567"
                      )
    profile_picture = models.ImageField(
                         upload_to='user_avatars/',
                         blank=True,
                         null=True
                      )
    bio             = models.TextField(blank=True, help_text="Short user bio or notes")

    # ——————————— Localization & Preferences ———————————
    timezone        = models.CharField(
                         max_length=32,
                         choices=[(tz, tz) for tz in pytz.common_timezones],
                         default='UTC'
                      )
    language        = models.CharField(
                         max_length=8,
                         default='en',
                         help_text="ISO 639-1 code, e.g. en, de, fr"
                      )
    settings        = models.JSONField(
                         blank=True,
                         null=True,
                         help_text="Arbitrary per-user settings (UI prefs, notifications…)"
                      )

    # ——————————— Security & Status ———————————
    is_verified     = models.BooleanField(
                         default=False,
                         help_text="Has the user confirmed their email?"
                      )
    two_factor_enabled = models.BooleanField(
                         default=False,
                         help_text="If True, enforce 2FA on login"
                      )

    # `date_joined`, `last_login`, `is_active` already come from AbstractUser

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
