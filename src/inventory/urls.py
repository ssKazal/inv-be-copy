from django.urls import path, include
from rest_framework import routers
from inventory.views import (
    GoodsViewset,
    BazarViewset,
    BazarGoodsViewset,
    users,
    get_user_info_from_token,
    verify_user_permission_from_token,
)

router = routers.DefaultRouter()
router.register(r"goods", GoodsViewset, basename="goods")
router.register(r"bazar", BazarViewset, basename="bazar")
router.register(r"bazar_goods", BazarGoodsViewset, basename="bazar_goods")


urlpatterns = [
    path("", include((router.urls, "inventory"), namespace="inventory_api")),
    path("users/", users, name="users"),
    path(
        "user-info-from-token/", get_user_info_from_token, name="user_info_from_token"
    ),
    path(
        "verify-user-permission-from-token/",
        verify_user_permission_from_token,
        name="verify_user_permission_from_token",
    ),
]
