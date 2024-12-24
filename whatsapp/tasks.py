from celery import shared_task
from .models import WhatsAppMessage
from twilio.rest import Client
from django.conf import settings


@shared_task
def send_whatsapp_message(sender, receiver, content):
    # Twilio client setup
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Send WhatsApp message
    client.messages.create(
        body=content,
        from_=f"whatsapp:{sender}",  # Replace with your Twilio WhatsApp sandbox number or your own Twilio number
        to=f"whatsapp:{receiver}",  # Send message to the receiver's WhatsApp number
    )
    message = WhatsAppMessage.objects.create(
        sender=sender, receiver=receiver, content=content, status="sent"
    )
    return f"Message {message.id} sent!"
