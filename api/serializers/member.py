from rest_framework import serializers
from api.models.member import Member


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'company', 'designation', 'password', 'bio',
                  'technology', 'company_email', 'company_phone', 'location', 'website_link', 'logo',
                  'registration_status', 'subscription_status', 'subscription_category', 'subscription_expiry',
                  'status', 'step', 'created_by', 'created_at', 'last_updated']
