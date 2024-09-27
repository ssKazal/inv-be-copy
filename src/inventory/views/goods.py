from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from inventory.serializers import GoodsSerializer, GoodsLogSerializer
from inventory.models import Goods, GoodsLog
from inventory.permissions import GoodsPermission
from inventory.custom.pagination import CustomPagination, CustomOneTimeGoodsPagination, \
    CustomOldOneTimeGoodsPagination
from inventory.custom.general_func import get_image_from_data_url

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class GoodsViewset(viewsets.ModelViewSet):
    serializer_class = GoodsSerializer
    permission_classes = [GoodsPermission]
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["name", "current_quantity"]
    ordering = ["-created_at"]  # Default ordering

    def get_queryset(self):
        goods_qs = cache.get("goods_qs")
        if not goods_qs:
            goods_qs = Goods.objects.all()
            cache.set("goods_qs", goods_qs, timeout=CACHE_TTL)

        return goods_qs.order_by("-created_at")

    def create(self, request):
        """
        Overriding create method
        """
        return Response(self._create_or_update(request, instance=None))

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def update(self, request, pk=None):
        """
        Overriding update method
        """
        instance = self.get_object()
        return Response(self._create_or_update(request, instance=instance))

    def _create_or_update(self, request, instance):
        """
        For creating or updating goods
        """
        data = request.data.copy()

        if data["icon"]:
            icon = get_image_from_data_url(data["name"], data["icon"])
            data["icon"] = icon
        if not instance:  # For creating
            serializer = self.get_serializer(data=data, context={"is_creating": True})
        else:  # For updating
            # Check if 'icon' is not present in the request data
            if not data["icon"]:
                data["icon"] = instance.icon  # Retain the existing icon
            serializer = self.get_serializer(instance, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return serializer.data

    @action(detail=True, methods=["GET"])
    def goods_log(self, request, pk=None):
        goods_obj = self.get_object()
        goods_logs = cache.get(f"goods_log_{goods_obj.id}")
        if not goods_logs:
            goods_logs = GoodsLog.objects.filter(goods_obj=goods_obj)
            cache.set(f"goods_log_{goods_obj.id}", goods_logs, timeout=CACHE_TTL)
        goods_logs = goods_logs.order_by("-id")

        paginator = CustomPagination()
        paginator.page_size = 5
        page = paginator.paginate_queryset(goods_logs, request)
        if page is not None:
            serializer = GoodsLogSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = GoodsLogSerializer(goods_logs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"], url_path='regular')
    def regular_goods(self, request):
        goods_qs = self.get_queryset().filter(is_one_time=False)

        # Use getlist directly without [0] since it's already a list
        skip_ids_for_search = self.request.GET.getlist("skip_ids_for_search", [])

        if skip_ids_for_search:
            # Use list comprehension without [0]
            skip_ids_as_int = [int(id_str) for id_str in skip_ids_for_search[0].split(',') if id_str]
            goods_qs = goods_qs.exclude(id__in=skip_ids_as_int)

        result_page = self.paginate_queryset(goods_qs)

        # Use the serializer_class without instantiation
        if result_page is not None:
            serializer = self.serializer_class(result_page, many=True)
            return self.get_paginated_response(serializer.data)

        # Always create a serializer instance
        serializer = self.serializer_class(goods_qs, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"], url_path='onetime')
    def onetime_goods(self, request):
        goods_qs = self.get_queryset().filter(is_one_time=True, has_purchased=False)

        # Use getlist directly without [0] since it's already a list
        skip_ids_for_search = self.request.GET.getlist("skip_ids_for_search", [])

        if skip_ids_for_search:
            # Use list comprehension without [0]
            skip_ids_as_int = [int(id_str) for id_str in skip_ids_for_search[0].split(',') if id_str]
            goods_qs = goods_qs.exclude(id__in=skip_ids_as_int)

        paginator = CustomOneTimeGoodsPagination()
        result_page = paginator.paginate_queryset(goods_qs, request)

        # Use the serializer_class without instantiation
        if result_page is not None:
            serializer = self.serializer_class(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Always create a serializer instance
        serializer = self.serializer_class(goods_qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"], url_path='old-onetime')
    def old_onetime_goods(self, request):
        goods_qs = self.get_queryset().filter(is_one_time=True, has_purchased=True)

        paginator = CustomOldOneTimeGoodsPagination()
        result_page = paginator.paginate_queryset(goods_qs, request)

        # Use the serializer_class without instantiation
        if result_page is not None:
            serializer = self.serializer_class(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Always create a serializer instance
        serializer = self.serializer_class(goods_qs, many=True)
        return Response(serializer.data)
