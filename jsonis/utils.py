import decimal
from json import JSONEncoder, JSONDecoder


class MyJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(MyJSONEncoder, self).default(o)

class MyJSONDecoder(JSONDecoder):
    pass