from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from api.models.administrator import Administrator
from api.models.member import Member


class UserJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_type = validated_token.get("user_type")
            if user_type == "admin":
                return Administrator.objects.get(id=validated_token["user_id"])
            elif user_type == "member":
                return Member.objects.get(id=validated_token["user_id"])
            else:
                raise AuthenticationFailed("Invalid user type in token.")
        except Administrator.DoesNotExist:
            raise AuthenticationFailed("No user found with this token.")
        except Member.DoesNotExist:
            raise AuthenticationFailed("No user found with this token.")
        except KeyError:
            raise AuthenticationFailed(
                'Invalid token. No "user_id" found in the token.'
            )
        except TypeError:
            raise AuthenticationFailed("Empty token. Please provide a valid JWT token.")
