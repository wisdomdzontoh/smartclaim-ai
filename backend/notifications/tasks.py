# notifications/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from claims.models import Claim

@shared_task
def send_claim_update_email(claim_id, new_status):
    """
    Send an email to the claim submitter when their claim status changes.
    """
    claim = Claim.objects.get(pk=claim_id)
    subject = f"Your claim '{claim.title}' is now {new_status}"
    message = (
        f"Hi {claim.user.get_full_name() or claim.user.username},\n\n"
        f"Your claim titled '{claim.title}' has been updated to '{new_status}'.\n\n"
        "Thanks,\nThe SmartClaim AI Team"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [claim.user.email],
        fail_silently=False,
    )
    return True
