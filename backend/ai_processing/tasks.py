# ai_processing/tasks.py
from celery import shared_task
from django.conf import settings
from claims.models import Claim
import openai

@shared_task
def run_ai_on_claim(claim_id):
    """
    Fetch the claim, call OpenAI to generate summary, tags, severity and fraud risk,
    then save back to the Claim.
    """
    claim = Claim.objects.get(pk=claim_id)

    # Example: generate a summary with GPT
    openai.api_key = settings.OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model    = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": "You summarize insurance claims."},
            {"role": "user", "content": claim.description},
        ],
        temperature=0.3,
    )
    summary = response.choices[0].message.content

    # (You could chain more calls to tag, score, etc.)
    claim.ai_summary       = summary
    claim.severity_score   = 0.5  # placeholder
    claim.fraud_risk_score = 0.1  # placeholder
    claim.save()

    return {'claim_id': claim_id, 'summary': summary[:50]}
