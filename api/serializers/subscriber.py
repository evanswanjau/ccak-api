import re

from rest_framework import serializers
from api.models.subscriber import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['id', 'email', 'created_at']

    @staticmethod
    def validate_email(email):
        """
        Validate the email field.

        Args:
            email (str): Email address.

        Returns:
            str: Validated email address.

        Raises:
            serializers.ValidationError: If the email is not valid or if it already exists.
        """
        # Perform email validation here
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise serializers.ValidationError("Invalid email address.")

        # Check if email already exists
        if Subscriber.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists.')
        return email
