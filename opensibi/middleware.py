from functools import wraps
from opensibi.jwt import JWTAuth
from opensibi.response import Response
import jwt

def jwtRequired(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            decode(args[0].headers.get('Authorization'))
        except jwt.ExpiredSignatureError:
            return Response.unauthorized(message="Token Expired")
        except jwt.InvalidTokenError:
            return Response.unauthorized(message="unauthorized")
        except Exception as e:
            return Response.unauthorized(message="unauthorized")  
        return fn(*args, **kwargs)
        
    return wrapper


def decode(token):
    token = str(token).split(' ')
    return JWTAuth().decode(token[1])


