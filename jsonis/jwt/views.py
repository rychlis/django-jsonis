from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from jsonis.views import JSONApiResponseMixin
from .utils import parse_token, JWTParseError


class JWTAuthorizationMixin(JSONApiResponseMixin):
    """JSON API mixin that enables JSON Web Token authorization

    FIXME: Deprecated, move to middleware & auth backend"""
    jwt_token_data = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            self.user = request.user
        else:
            try:
                auth_prefix, auth_token = request.META['HTTP_AUTHORIZATION'].split(' ')
                if auth_prefix != 'Bearer':
                    return self.render_api_error_response('Not authenticated - Bad authorization header prefix',
                                                          status=401)
                jwt_token_data = parse_token(auth_token)
            except ValueError:
                return self.render_api_error_response('Not authenticated - Bad authorization header format', status=401)
            except KeyError:
                return self.render_api_error_response('Not authenticated - Missing authorization header', status=401)
            except JWTParseError as e:
                return self.render_api_error_response('Not authenticated - %s' % e, status=401)

            error_response = self._check_token_data(jwt_token_data)
            if error_response is not None:
                return error_response
        return super(JWTAuthorizationMixin, self).dispatch(request, *args, **kwargs)

    def _check_token_data(self, jwt_token_data):
        """Parsed token data checks. Returns a Response if there is an error, None otherwise"""
        try:
            self.user = get_user_model().objects.get(pk=self.jwt_token_data['id'])
        except (TypeError, KeyError):
            return self.render_api_error_response('Not authenticated - Bad authorization header data', status=401)
        except get_user_model().DoesNotExist:
            return self.render_api_error_response('Not authenticated - User not found', status=401)
        self.jwt_token_data = jwt_token_data
        return None