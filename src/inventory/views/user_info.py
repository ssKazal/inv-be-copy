from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from django.contrib.auth import get_user_model
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)
User = get_user_model()

@api_view(["GET"])
def get_user_info_from_token(request):
    user_data = {}
    if authentication.JWTAuthentication().authenticate(request):
        user_obj = authentication.JWTAuthentication().authenticate(request)[0]
        if user_obj:
            user_data["id"] = user_obj.id
            user_data["username"] = user_obj.username
            user_data["is_superuser"] = user_obj.is_superuser
            user_data["email"] = user_obj.email
            user_data["groups"] = user_obj.groups.values_list("name", flat=True)

            user_permissions = []
            user_group = user_obj.groups.all().first()
            if user_group:
                user_permissions += user_group.permissions.all().values_list(
                    "codename", flat=True
                )
            user_data["permissions"] = user_permissions
            return Response(user_data, status=200)
    return Response(user_data, status=404)


@api_view(["POST"])
def verify_user_permission_from_token(request):
    if request.META.get("HTTP_AUTHORIZATION", False):
        user_obj = authentication.JWTAuthentication().authenticate(request)[0]
        which_perm = request.data.get("which_perm", None)
        if which_perm:
            if user_obj.has_perm(which_perm):
                return Response({"status": True})
    return Response({"status": False}, status=401)

@api_view(["GET"])
def users(request):
    user_info = User.objects.all().values("id", "username")
    return Response(user_info, status=200)

