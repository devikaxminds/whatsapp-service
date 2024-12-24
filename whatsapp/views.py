from django.shortcuts import render

# Create your views here.
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WhatsAppMessage
from .serializers import WhatsAppMessageSerializer
from .tasks import send_whatsapp_message
from twilio.twiml.messaging_response import MessagingResponse
from rest_framework.exceptions import APIException, ValidationError

# default logger
logger = logging.getLogger("whatsapp_integration")


class SendMessageView(APIView):
    """
    Send a WhatsApp message.

    This view is responsible for accepting a POST request to send a WhatsApp message.
    It validates the incoming data, and if valid, it queues the message for asynchronous sending using Celery.
    In case of missing fields or validation errors, appropriate error responses are raised.
    If an unexpected error occurs, it is logged and an APIException is raised.

    Methods:
        post(request):
            Handles POST requests to send a WhatsApp message. It validates the request data, queues the message using Celery,
            and returns a response indicating the status of the request. If there are any issues, it raises appropriate exceptions.

    Exceptions:
        - KeyError: Raised if required fields are missing in the request data.
        - ValidationError: Raised if the request data is invalid based on the serializer.
        - Exception: Catches all other unexpected errors and raises a general APIException.
    """

    def post(self, request):
        try:
            # Deserialize incoming data using the serializer
            serializer = WhatsAppMessageSerializer(data=request.data)
            # Validate the data
            if not serializer.is_valid():
                logger.error(f"Invalid data: {serializer.errors}")
                return Response(
                    {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )

            data = serializer.validated_data
            # Send the WhatsApp message asynchronously using Celery
            send_whatsapp_message.delay(
                data["sender"], data["receiver"], data["content"]
            )
            logger.info(f"Message queued successfully for {data['receiver']}")
            return Response({"status": "Message sent"}, status=status.HTTP_202_ACCEPTED)
        except KeyError as e:
            # Log the error and raise an exception
            logger.error(f"Missing required field: {str(e)}")
            raise APIException(f"Missing required field: {str(e)}")

        except ValidationError as e:
            # Reraise ValidationError to be handled by DRF automatically
            logger.error(f"Validation error: {str(e)}")
            raise e

        except Exception as e:
            # Log the unexpected exception
            logger.error(f"Unexpected error occurred: {str(e)}")
            raise APIException(f"An unexpected error occurred: {str(e)}")


class WebhookView(APIView):
    """
    Webhook to receive and process incoming messages from Twilio.

    - Extracts the message content and sender details.
    - Saves the message to the database.

    Expected incoming data format:
    {
        'Body': 'Message content',
        'From': 'Sender phone number',
        'To': 'Receiver phone number'
    }
    """

    def post(self, request):
        try:
            # Extract the incoming data from the request
            incoming_message = request.data.get("Body", "")
            sender = request.data.get("From", "")

            receiver = request.data.get("To", "")  # Receiver's number (Twilio number)
            sender_number = (
                sender.replace("whatsapp:", "")
                if sender.startswith("whatsapp:")
                else sender
            )
            receiver_number = (
                receiver.replace("whatsapp:", "")
                if receiver.startswith("whatsapp:")
                else receiver
            )

            # Store the message in the database
            WhatsAppMessage.objects.create(
                sender=sender_number,
                receiver=receiver_number,
                content=incoming_message,
                status="received",
            )
            logger.info(
                f"Received message from {sender_number} to {receiver_number}: {incoming_message} and stored in database"
            )
            return Response(
                {"status": "Message received"}, status=status.HTTP_202_ACCEPTED
            )

        except Exception as e:
            logger.error(f"Error processing incoming message: {str(e)}")
            return Response(
                {"error": "An error occurred while receiving the message"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
