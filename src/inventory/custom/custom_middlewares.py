import threading
from django.utils.deprecation import MiddlewareMixin


class GetCurrentUserMiddleWare(MiddlewareMixin):
    thread_local = threading.local()

    def process_request(self, request):
        GetCurrentUserMiddleWare.thread_local.current_user_token = request.META.get(
            "HTTP_AUTHORIZATION", None
        )
