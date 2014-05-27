from django.conf import settings

from django.http import HttpResponse
from django.views.generic.edit import BaseFormView

from .utils import MyJSONEncoder, MyJSONDecoder, lazyprop

class CharsetHttpResponse(HttpResponse):
    """HttpResponse that will append charset info into Content-Type header"""
    charset = settings.DEFAULT_CHARSET

    def __init__(self, *args, **kwargs):
        if 'content_type' in kwargs and kwargs['content_type'].find('charset=') == -1:
            kwargs['content_type'] = '%s; charset=%s' % (kwargs['content_type'], self.charset)

        super(CharsetHttpResponse, self).__init__(*args, **kwargs)

class JSONResponse(CharsetHttpResponse):
    """Simple response class that will automatically serialize encode data to JSON"""

    def __init__(self, content_data, json_encoder=MyJSONEncoder, *args, **kwargs):
        encoder = json_encoder(ensure_ascii=False, encoding=self.charset)
        self.content_data = content_data
        kwargs.setdefault('content_type', 'application/json')

        super(JSONResponse, self).__init__(encoder.encode(self.content_data), *args, **kwargs)

class JSONResponseMixin(object):
    """Mixin providing render_json_response returning the JSONResponse"""
    def render_json_response(self, content_data):
        return JSONResponse(content_data)

class JSONPResponse(CharsetHttpResponse):
    def __init__(self, content_data, callback, json_encoder=MyJSONEncoder, *args, **kwargs):
        encoder = json_encoder(ensure_ascii=False, encoding=self.charset)
        self.content_data = content_data
        kwargs.setdefault('content_type', 'application/javascript')

        super(JSONPResponse, self).__init__('%s(%s)' % (callback, encoder.encode(self.content_data)), *args, **kwargs)

class JSONPResponseMixin(object):
    """JSONP Response mixin that will fallback to JSON response if there is no callback supplied"""
    def render_jsonp_response(self, data):
        try:
            return JSONPResponse(data, self.request.REQUEST['callback'])
        except KeyError:
            return JSONResponse(data)

class JSONApiResponse(JSONResponse):
    def __init__(self, content_data=None, status_msg='ok', json_encoder=MyJSONEncoder, *args, **kwargs):
        if content_data is None:
            content_data = {}
        content_data['status'] = status_msg
        super(JSONApiResponse, self).__init__(content_data, json_encoder, *args, **kwargs)

class JSONApiErrorResponse(JSONApiResponse):
    status_code = 400

    def __init__(self, error_msg, content_data=None, status_msg='fail', json_encoder=MyJSONEncoder, *args, **kwargs):
        if content_data is None:
            content_data = {}
        content_data['error'] = error_msg
        super(JSONApiErrorResponse, self).__init__(content_data, status_msg, json_encoder, *args, **kwargs)

class JSONApiResponseMixin(object):
    """Mixin providing JSON Api view functionality returning JSONApiResponse"""

    @lazyprop
    def payload_data(self):
        """Decode received request data"""
        if self.request.META.get('CONTENT_TYPE', '').find('application/json') == 0:
            decoder = MyJSONDecoder(encoding='utf-8')
            return decoder.decode(self.request.body)
        else:
            return self.request.POST

    def render_api_response(self, content_data, **kwargs):
        return JSONApiResponse(content_data, **kwargs)

    def render_api_error_response(self, error_message, content_data=None, **kwargs):
        return JSONApiErrorResponse(error_message, content_data, **kwargs)

class JSONApiLoginRequiredMixin(JSONApiResponseMixin):
    """JSONApiResponseMixin that will check user authorization"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return self.user_unauthorized()
        return super(JSONApiLoginRequiredMixin, self).dispatch(request, *args, **kwargs)

    def user_unauthorized(self):
        return self.render_api_error_response('Not authenticated', status=401)

class JSONApiFormView(JSONApiResponseMixin, BaseFormView):
    def dispatch(self, request, *args, **kwargs):
        return super(JSONApiFormView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(JSONApiFormView, self).get_form_kwargs()
        if 'data' in kwargs:
            kwargs['data'] = self.payload_data
        return kwargs

    def get(self, request, *args, **kwargs):
        return self.render_api_error_response('Method not allowed', status=405)

    def form_valid(self, form):
        raise NotImplementedError

    def form_invalid(self, form):
        return self.render_api_error_response(dict(form.errors.iteritems()))