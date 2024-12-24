from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from whatsapp.models import WhatsAppMessage
from whatsapp.serializers import WhatsAppMessageSerializer


class SendMessageViewTest(APITestCase):
    """Test the SendMessageView for sending WhatsApp messages."""

    @patch("whatsapp.views.send_whatsapp_message.delay")  # Mock Celery task
    def test_send_message_success(self, mock_send_message):
        """Test sending a message with valid data."""
        # Sample valid data
        data = {
            "sender": "+1234567890",
            "receiver": "+0987654321",
            "content": "Hello, this is a test message",
        }

        # Send a POST request to the SendMessageView
        response = self.client.post("/whatsapp/send-message/", data, format="json")

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        # Assert the response contains the expected message
        self.assertEqual(response.data["status"], "Message queued")

        # Assert the Celery task was called
        mock_send_message.assert_called_once_with(
            data["sender"], data["receiver"], data["content"]
        )

    @patch("whatsapp.views.send_whatsapp_message.delay")
    def test_send_message_missing_field(self, mock_send_message):
        """Test sending a message with missing fields (e.g., content)."""
        # Incomplete data (missing 'content')
        data = {"sender": "+1234567890", "receiver": "+0987654321"}

        # Send a POST request
        response = self.client.post("/whatsapp/send-message/", data, format="json")

        # Assert the response status code for a bad request (400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert the Celery task was not called
        mock_send_message.assert_not_called()

    @patch("whatsapp.views.send_whatsapp_message.delay")
    def test_send_message_invalid_data(self, mock_send_message):
        """Test sending a message with invalid data (e.g., invalid phone number)."""
        # Invalid data (invalid phone number format)
        data = {
            "sender": "invalid_sender",
            "receiver": "invalid_receiver",
            "content": "Test message",
        }

        # Send a POST request
        response = self.client.post("/whatsapp/send-message/", data, format="json")

        # Assert the response status code for validation errors (400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert the Celery task was not called
        mock_send_message.assert_not_called()

    @patch("whatsapp.views.send_whatsapp_message.delay")
    def test_send_message_unexpected_error(self, mock_send_message):
        """Test sending a message where an unexpected error occurs."""
        # Mock Celery to raise an unexpected error
        mock_send_message.side_effect = Exception("Unexpected error")

        # Sample valid data
        data = {
            "sender": "+1234567890",
            "receiver": "+0987654321",
            "content": "Hello, this is a test message",
        }

        # Send a POST request
        response = self.client.post("/whatsapp/send-message/", data, format="json")

        # Assert the response status code for internal server error (500)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Assert the error message is as expected
        self.assertIn("An unexpected error occurred", response.data["detail"])
