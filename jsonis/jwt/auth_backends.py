from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from .utils import parse_token, JWTParseError

class JWTAuthenticationBackend(ModelBackend):
    """Custom django authentication backend using JWT"""
    def authenticate(self, authentication_token=None, **kwargs):
        UserModel = get_user_model()
        if authentication_token is None:
            return
        try:
            token_data = parse_token(authentication_token)
            return UserModel._default_manager.get(pk=token_data['id'])
        except JWTParseError:
            pass
        except UserModel.DoesNotExist:
            pass