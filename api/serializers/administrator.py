import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from api.models.administrator import Administrator


class AdministratorSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Administrator model.
    Provides validation and serialization/deserialization of Administrator objects.
    """

    class Meta:
        model = Administrator
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "password",
            "role",
            "status",
            "created_by",
            "created_at",
            "author",
            "last_updated",
        ]

    def validate_email(self, email):
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
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            raise serializers.ValidationError("Invalid email address.")

        # check if email already exists while creating an administrator
        if self.instance is None and Administrator.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")

        # check if email already exists while updating am administrator
        if (
            self.instance
            and Administrator.objects.filter(email=email)
            .exclude(id=self.instance.id)
            .exists()
        ):
            raise serializers.ValidationError("Email already exists.")
        return email

    def update(self, instance, validated_data):
        """
        Update an existing administrator instance.

        Hashes the password using bcrypt if it is updated.

        Args:
            instance (Administrator): The existing administrator instance.
            validated_data (dict): Validated data for updating the administrator.

        Returns:
            Administrator: The updated administrator instance.
        """
        # Hash the password using bcrypt if it is updated
        if "password" in validated_data:
            password = validated_data.pop("password")
            validated_data["password"] = make_password(password)
        return super().update(instance, validated_data)
