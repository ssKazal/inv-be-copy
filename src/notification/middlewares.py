import re
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.backends import TokenBackend

User = get_user_model()

@database_sync_to_async
def get_user_from_token(token):
    print("token", token)
    # user_id=access_token_obj['user_id']
    user_id=1
    user=User.objects.filter(id=user_id).first()
    if user:
        return user

    return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        token_key = None

        if b'authorization' in headers:
            token_key = headers[b'authorization'].decode().split()[1]

        elif scope.get('query_string'):
            try:
                data = scope['query_string'].decode().split()[0]
                token_key = re.search(r'Authorization=([\w\d]+)', data).group(1)
            except:
                pass

        scope['user'] = AnonymousUser() if token_key is None else await get_user_from_token(token_key)

        return await super().__call__(scope, receive, send)

from urllib.parse import parse_qs
class QueryParamsMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        scope = dict(scope)

        scope["query_params"] = parse_qs(scope["query_string"].decode())

        return await super().__call__(scope, receive, send)    
