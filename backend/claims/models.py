from django.db import models
from django.utils import timezone
from accounts.models import User
from companies.models import Company

class Claim(models.Model):
    # Core
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    company     = models.ForeignKey(Company, on_delete=models.CASCADE)
    title       = models.CharField(max_length=255)
    description = models.TextField()

    # Workflow
    STATUS_CHOICES = [
        ('new',        'New'),
        ('in_review',  'In Review'),
        ('approved',   'Approved'),
        ('rejected',   'Rejected'),
        ('closed',     'Closed'),
    ]
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority    = models.PositiveSmallIntegerField(
                     default=3,
                     help_text="1=High, 5=Low"
                  )
    assigned_to = models.ForeignKey(
                     User,
                     on_delete=models.SET_NULL,
                     null=True, blank=True,
                     related_name="assigned_claims",
                     limit_choices_to={'role__in': ['claims_handler','supervisor']}
                  )

    # AI-assisted fields
    ai_summary         = models.TextField(blank=True, null=True)
    ai_tags            = models.JSONField(blank=True, null=True)
    severity_score     = models.FloatField(blank=True, null=True)
    fraud_risk_score   = models.FloatField(blank=True, null=True)

    # Timestamps & audit
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    resolved_at   = models.DateTimeField(blank=True, null=True)

    def mark_resolved(self):
        self.status = 'closed'
        self.resolved_at = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        is_update = self.pk is not None
        old_status = None
        if is_update:
            # fetch the previous status from the DB
            old_status = Claim.objects.filter(pk=self.pk).values_list('status', flat=True).first()

        super().save(*args, **kwargs)

        # if this was an update and status changed, enqueue notification
        if is_update and old_status and old_status != self.status:
            # import here to avoid circular dependency
            from notifications.tasks import send_claim_update_email
            send_claim_update_email.delay(self.id, self.status)

    def __str__(self):
        return f"{self.title} [{self.get_status_display()}]"


class Document(models.Model):
    claim       = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='documents')
    file        = models.FileField(upload_to='claim_documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
