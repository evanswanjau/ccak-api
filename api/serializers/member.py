import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from api.models.member import Member


class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Member model.
    Provides validation and serialization/deserialization of Member objects.
    """

    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'company', 'designation', 'password',
                  'bio', 'technology', 'company_email', 'company_phone', 'location', 'website_link', 'logo',
                  'registration_status', 'subscription_status', 'subscription_category', 'subscription_expiry',
                  'status', 'step', 'agree_to_terms', 'created_by', 'created_at', 'last_updated']

    def validate_email(self, email):
        print(self.instance)
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

        # check if email already exists while creating a member
        if self.instance is None and Member.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists.')

        # check if email already exists while updating a member
        if self.instance and Member.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError('Email already exists.')
        return email

    def validate_phone_number(self, phone_number):
        """
        Validate the phone_number field.

        Args:
            phone_number (str): Phone number.

        Returns:
            str: Validated phone number.

        Raises:
            serializers.ValidationError: If the phone number is not valid or if it already exists.
        """
        # Perform phone number validation here
        if not re.match(r'^\+?\d{1,3}[-.\s]?\(?\d{1,3}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$', phone_number):
            raise serializers.ValidationError("Invalid phone number.")

        # check if email already exists while creating a member
        if self.instance is None and Member.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError('Email already exists.')

        # check if email already exists while updating a member
        if self.instance and Member.objects.filter(phone_number=phone_number).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError('Email already exists.')
        return phone_number

    def update(self, instance, validated_data):
        """
        Update an existing member instance.

        Hashes the password using bcrypt if it is updated.

        Args:
            instance (Member): The existing member instance.
            validated_data (dict): Validated data for updating the member.

        Returns:
            Member: The updated member instance.
        """
        # Hash the password using bcrypt if it is updated
        if 'password' in validated_data:
            password = validated_data.pop('password')
            validated_data['password'] = make_password(password)
        return super().update(instance, validated_data)
