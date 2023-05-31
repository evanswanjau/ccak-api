import bcrypt

from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from api.models.member import Member


@api_view(['POST'])
def member_login(request):
    """
    Authenticate a member and generate JWT tokens.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - If the login is successful, returns the generated tokens.
    - If the login fails, returns an error response.

    HTTP Methods: POST
    """
    email = request.data.get('email')
    password = request.data.get('password')

    if email and password:
        member = Member.objects.filter(email=email).first()

        if member and check_password(password, member.password):
            # Generate tokens
            refresh = RefreshToken.for_user(member)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
