import decimal
from json import JSONEncoder, JSONDecoder


class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(MyJSONEncoder, self).default(o)

class MyJSONDecoder(JSONDecoder):
    pass

# Lazy evaluation utils
def lazyprop(fn, prefix='_lazy_'):
    """Lazy property decorator

    Property is evaluated only on first use and then cached in _lazy_*propname* attribute"""
    attr_name = prefix + fn.__name__

    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop