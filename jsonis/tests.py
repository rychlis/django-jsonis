import json

from .utils import JSONEncoder
from django.test import Client, TestCase

class JSONTestClient(Client):
    """Test client for JSON requests"""

    def _encode_data(self, data, content_type, **kwargs):
        """Encode POST data to JSON for json content type"""
        if content_type.find('application/json') == 0:
            return json.dumps(data, cls=JSONEncoder)
        else:
            return super(JSONTestClient, self)._encode_data(data, content_type, **kwargs)

    def post(self, path, content_type='application/json; charset=utf-8', **kwargs):
        """Only changing content_type default value"""
        return super(JSONTestClient, self).post(path, content_type=content_type, **kwargs)

    def put(self, path, content_type='application/json; charset=utf-8', **kwargs):
        """Only changing content_type default value"""
        return super(JSONTestClient, self).put(path, content_type=content_type, **kwargs)

class JSONTestCase(TestCase):
    client_class = JSONTestClient