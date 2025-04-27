from django.db import models
import pytz

class Company(models.Model):
    # Core info
    name             = models.CharField(max_length=255)
    website          = models.URLField(blank=True, null=True)
    contact_email    = models.EmailField(blank=True, null=True)
    contact_phone    = models.CharField(
                         max_length=30,
                         blank=True,
                         help_text="E.g. +1-555-123-4567"
                      )
    address          = models.TextField(blank=True)

    # Business metadata
    industry         = models.CharField(
                         max_length=100,
                         blank=True,
                         help_text="E.g. Insurance, Manufacturing, Retail"
                      )
    timezone         = models.CharField(
                         max_length=32,
                         choices=[(tz, tz) for tz in pytz.common_timezones],
                         default="UTC"
                      )
    default_language = models.CharField(
                         max_length=8,
                         default="en",
                         help_text="ISO 639-1, e.g. en, de, fr"
                      )

    # Subscription / plan data
    PLAN_CHOICES = [
      ("free",    "Free"),
      ("basic",   "Basic"),
      ("premium", "Premium"),
      ("enterprise", "Enterprise"),
    ]
    subscription_plan       = models.CharField(
                                max_length=20,
                                choices=PLAN_CHOICES,
                                default="free"
                             )
    subscription_expires_at = models.DateTimeField(
                                blank=True,
                                null=True,
                                help_text="When the current plan ends"
                             )
    is_active               = models.BooleanField(
                                default=True,
                                help_text="Deactivate to block company access"
                             )

    # Branding & customizations
    logo                    = models.ImageField(
                                upload_to="company_logos/",
                                blank=True,
                                null=True
                             )
    primary_color_hex       = models.CharField(
                                max_length=7,
                                blank=True,
                                help_text="Brand color, e.g. #1A73E8"
                             )
    settings                = models.JSONField(
                                blank=True,
                                null=True,
                                help_text="Ad-hoc company settings (email templates, workflows…)"
                             )

    # Timestamps
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
