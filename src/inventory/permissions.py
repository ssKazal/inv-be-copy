from rest_framework import permissions


class GoodsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if view.action == "list":
                return request.user.has_perm("inventory.view_goods")
            elif view.action == "create":
                return request.user.has_perm("inventory.add_goods")
            elif view.action == "retrieve":
                return request.user.has_perm("inventory.view_goods")
            elif view.action in ["update", "partial_update"]:
                return request.user.has_perm("inventory.change_goods")
            elif view.action == "destroy":
                return request.user.has_perm("inventory.delete_goods")
            elif view.action == "goods_log":
                return request.user.has_perm("inventory.view_goodslog")
            elif view.action == "regular_goods":
                return request.user.has_perm("inventory.view_goods")
            elif view.action == "onetime_goods":
                return request.user.has_perm("inventory.view_goods")
            elif view.action == "old_onetime_goods":
                return request.user.has_perm("inventory.view_goods")

        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if view.action == "retrieve":
                return request.user.has_perm("inventory.view_goods")
            elif view.action in ["update", "partial_update"]:
                return request.user.has_perm("inventory.change_goods")
            elif view.action == "destroy":
                return request.user.has_perm("inventory.delete_goods")
            elif view.action == "goods_log":
                return request.user.has_perm("inventory.view_goodslog")

        return False
