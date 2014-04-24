from __future__ import absolute_import

import jwt

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .views import JSONApiResponseMixin


class JWTAuthorizationMixin(JSONApiResponseMixin):
    """JSON API mixin that enables JSON Web Token authorization"""
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            self.user = request.user
        else:
            try:
                auth_prefix, auth_token = request.META['HTTP_AUTHORIZATION'].split(' ')
                if auth_prefix != 'Bearer':
                    raise ValueError
                token_data = jwt.decode(auth_token, settings.FIREBASE_SECRET)
            except KeyError:
                return self.render_api_error_response('Not authenticated - Missing authorization header', status=401)
            except ValueError:
                return self.render_api_error_response('Not authenticated - Bad authorization header', status=401)
            except jwt.DecodeError:
                return self.render_api_error_response('Not authenticated - Bad authorization header (decode failed)',
                                                      status=401)
            except jwt.ExpiredSignature:
                return self.render_api_error_response('Not authenticated - Expired authorization header', status=401)

            try:
                self.user = get_user_model().objects.get(pk=token_data['d']['id'])
            except (TypeError, KeyError):
                return self.render_api_error_response('Not authenticated - Bad authorization header data', status=401)
            except get_user_model().DoesNotExist:
                return self.render_api_error_response('Not authenticated - User not found', status=401)
        return super(JWTAuthorizationMixin, self).dispatch(request, *args, **kwargs)