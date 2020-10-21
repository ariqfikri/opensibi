from functools import wraps
from opensibi.jwt import JWTAuth
from rest_framework.response import Response
import jwt

def jwtRequired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            decode(args[0].headers.get('Authorization'))
        except jwt.ExpiredSignatureError:
            return Response(data="Token expired. Get new one")
        except jwt.InvalidTokenError:
            return Response(data="Invalid Token")    
        return fn(*args, **kwargs)
    return wrapper


def decode(token):
    token = str(token).split(' ')
    return JWTAuth().decode(token[1])