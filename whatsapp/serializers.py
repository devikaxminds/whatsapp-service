from rest_framework import serializers
from .models import WhatsAppMessage
import re


class WhatsAppMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhatsAppMessage
        fields = "__all__"

    def validate_sender(self, value):
        """Validate sender phone number format."""
        if not re.match(r"^\+?[0-9]\d{1,14}$", value):  # E.164 phone number format
            raise serializers.ValidationError("Invalid sender phone number format.")
        return value

    def validate_receiver(self, value):
        """Validate receiver phone number format."""
        if not re.match(r"^\+?[0-9]\d{1,14}$", value):  # E.164 phone number format
            raise serializers.ValidationError("Invalid receiver phone number format.")
        return value
