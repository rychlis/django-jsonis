import jwt

from django.conf import settings

class JWTParseError(Exception):
    pass

class JWTDecodeError(JWTParseError):
    pass

class JWTExpiredError(JWTParseError):
    pass

class JWTNoDataError(JWTDecodeError):
    pass

def parse_token(auth_token):
    """Parser given JSON Web Token and returns contained data"""
    try:
        decoded_token = jwt.decode(auth_token, settings.FIREBASE_SECRET)
    except (jwt.DecodeError, ValueError):
        raise JWTDecodeError('Decoding of authorization token failed')
    except jwt.ExpiredSignature:
        raise JWTExpiredError('Expired authorization token')

    try:
        return decoded_token['d']
    except (TypeError, KeyError):
        raise JWTNoDataError('No data in authorization token')
