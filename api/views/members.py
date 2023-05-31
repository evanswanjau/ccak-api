from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from api.models.member import Member
from api.serializers.member import MemberSerializer
from api.utils.email import send_email


class MemberView(APIView):
    """
    API endpoint for managing members.

    Methods:
    - GET: Retrieve all members or a specific member by their member ID.
    - POST: Create a new member.
    - PUT: Update an existing member by their member ID.
    - DELETE: Delete an existing member by their member ID.
    """

    def get(self, request, member_id=None):
        """
        Retrieve all members or a specific member by their member ID.

        Parameters:
        - request: The HTTP request object.
        - member_id: The ID of the member to retrieve (optional).

        Returns:
        - If member_id is provided, returns the serialized member data.
        - If member_id is None, returns serialized data for all members.

        HTTP Methods: GET
        """
        if member_id is not None:
            return self.get_single_member(member_id)
        else:
            return self.get_all_members()

    def get_single_member(self, member_id):
        """
        Retrieve details of a member by their member ID.

        Parameters:
        - member_id: The ID of the member to retrieve.

        Returns:
        - If the member exists, returns the serialized member data.
        - If the member does not exist, returns an error response.
        """
        try:
            member = Member.objects.get(pk=member_id)
            serializer = MemberSerializer(member)
            return Response(serializer.data)
        except Member.DoesNotExist:
            return Response({"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND)

    def get_all_members(self):
        """
        Retrieve all members.

        Returns:
        - Serialized data for all members.
        """
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new member.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - If the member is created successfully, returns the generated token.
        - If the member data is invalid, returns an error response.

        HTTP Methods: POST
        """
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            # Salt and hash the password
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)

            # save data
            member = serializer.save()

            # generate token
            token = self.generate_token(member)

            # Send verification email to the member
            self.send_verification_email(member, token)

            return Response({"token": token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, member_id):
        """
        Update an existing member by their member ID.

        Parameters:
        - request: The HTTP request object.
        - member_id: The ID of the member to update.

        Returns:
        - If the member exists and the data is valid, returns the updated member data.
        - If the member does not exist or the data is invalid, returns an error response.

        HTTP Methods: PUT
        """
        try:
            member = Member.objects.get(pk=member_id)
        except Member.DoesNotExist:
            return Response({"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, member_id):
        """
        Delete an existing member by their member ID.

        Parameters:
        - request: The HTTP request object.
        - member_id: The ID of the member to delete.

        Returns:
        - If the member exists, deletes the member and returns a success response.
        - If the member does not exist, returns an error response.

        HTTP Methods: DELETE
        """
        try:
            member = Member.objects.get(pk=member_id)
        except Member.DoesNotExist:
            return Response({"error": "Member not found."}, status=status.HTTP_404_NOT_FOUND)

        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def generate_token(user):
        """
        Generate an authentication token for a member.

        Parameters:
        - member: The member object.

        Returns:
        - The generated token object.

        """
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

    @staticmethod
    def send_verification_email(member, token):
        """
        Send a verification email to the member.

        Parameters:
        - recipient_email: The email address of the recipient.
        - verification_link: The link for email verification.

        """
        email_subject = "Welcome to The Clean Cooking Alliance Kenya"
        email_message = f"Dear {member.first_name},\n\nThank you for registering on YourApp. " \
                        f"Your account has been created successfully. Please click the following " \
                        f"link to verify your email:"
        return send_email(member.email, email_subject, email_message)
