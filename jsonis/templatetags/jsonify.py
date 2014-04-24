from django.conf import settings
from django.template import Library

from ..utils import MyJSONEncoder

register = Library()

encoder = MyJSONEncoder(ensure_ascii=False, encoding=settings.DEFAULT_CHARSET)

@register.filter
def jsonify(obj):
    return encoder.encode(obj)