from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from api.models.administrator import Administrator
from api.models.member import Member


class AdministratorJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            return Administrator.objects.get(id=validated_token["user_id"])
        except Administrator.DoesNotExist:
            raise AuthenticationFailed('No administrator found with this token.')
        except KeyError:
            raise AuthenticationFailed('Invalid token. No "user_id" found in the token.')
        except TypeError:
            raise AuthenticationFailed('Empty token. Please provide a valid JWT token.')


class UserJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            return Administrator.objects.get(id=validated_token["user_id"])
        except Administrator.DoesNotExist:
            pass  # Administrator not found, continue to member authentication
        except KeyError:
            raise AuthenticationFailed('Invalid token. No "user_id" found in the token.')
        except TypeError:
            raise AuthenticationFailed('Empty token. Please provide a valid JWT token.')

        try:
            return Member.objects.get(id=validated_token["user_id"])
        except Member.DoesNotExist:
            raise AuthenticationFailed('No user found with this token.')
        except KeyError:
            raise AuthenticationFailed('Invalid token. No "user_id" found in the token.')
        except TypeError:
            raise AuthenticationFailed('Empty token. Please provide a valid JWT token.')
