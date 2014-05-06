from django.contrib.auth import authenticate, login, get_user_model
from django.core.exceptions import ImproperlyConfigured

class JWTAuthMiddleware(object):
    """Authentication Middleware that checks for a JSON Web Token in the Authorization header

    JWTAuthenticationBackend needs to be added to AUTHENTICATION_BACKENDS as well"""

    # Used HTTP Header
    header = 'HTTP_AUTHORIZATION'

    # Required header prefix
    required_auth_prefix = 'Bearer'

    # Login user after successful authentication
    login_user = False

    def process_request(self, request):
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The JWT auth middleware requires the authentication middleware to be installed. Edit your"
                " MIDDLEWARE_CLASSES setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the JWTAuthMiddleware class.")

        try:
            auth_prefix, auth_token = request.META[self.header].split(' ')
            if auth_prefix != self.required_auth_prefix:
                raise ValueError

            user = authenticate(authentication_token=auth_token)
            if user:
                request.user = user
                if self.login_user:
                    login(request, user)

        except KeyError:
            # There is no self.header
            pass
        except ValueError:
            # Header prefix doesn't match
            pass
