from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Q
from django.db import transaction
from inventory.serializers import BazarSerializer, BazarGoodsSerializer
from inventory.models import Goods, Bazar, BazarGoods
from inventory.permissions import GoodsPermission
from inventory.custom.pagination import BazarGoodsPagination


class BazarViewset(viewsets.ModelViewSet):
    serializer_class = BazarSerializer
    # permission_classes = [GoodsPermission]
    queryset = Bazar.objects.all().order_by("-created_at")

    @action(detail=False, methods=['GET'], url_path='ongoing')
    def ongoing_bazar(self, request):
        bazar_obj = self.get_queryset().filter(status__in=["created", "started", "end"]).first()
        if bazar_obj:
            serializer = self.get_serializer(bazar_obj)
            return Response(serializer.data)
        
        return Response(None)
    
    @action(detail=False, methods=['GET'], url_path='selectable-goods')
    def selectable_goods(self, request):
        # We need 'label' field to show data in React search&select input field.
        goods_name_list = Goods.objects.filter(has_purchased=False).annotate(label=F('name')).values("label", "name", "measurement_type", "goods_type")
        return Response(goods_name_list)
    
    @action(detail=True, methods=['GET'], url_path='list')
    def bazar_list(self, request, pk=None):

        # We are ignoring purchased one time bazar from list
        bazar_goods = BazarGoods.objects.filter((Q(is_one_time=False) | Q(is_one_time=True, has_purchased=False)), bazar_obj=self.get_object()).order_by('-created_at')

        paginator = BazarGoodsPagination()
        page = paginator.paginate_queryset(bazar_goods, request)

        # Use the serializer_class without instantiation
        if page is not None:
            serializer = BazarGoodsSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Always create a serializer instance
        serializer = BazarGoodsSerializer(bazar_goods, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'], url_path='purchase-all')
    def purchase_all_bazar(self, request, pk=None):
        bazar_goods = BazarGoods.objects.filter(bazar_obj=self.get_object())
        bazar_goods.update(has_purchased=True)
        paginator = BazarGoodsPagination()
        page = paginator.paginate_queryset(bazar_goods.order_by("created_at"), request)

        # Use the serializer_class without instantiation
        if page is not None:
            serializer = BazarGoodsSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Always create a serializer instance
        serializer = BazarGoodsSerializer(bazar_goods.order_by("created_at"), many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['POST'], url_path='update-goods-list')
    def update_goods_list(self, request, pk=None):
        bazar_obj = self.get_object()
        if not bazar_obj.added_with_goods_list:
            bazar_goods = self.get_object().bazargoods_set.all()
            goods_names = [goods.name for goods in bazar_goods]
            
            existing_goods = Goods.objects.filter(name__in=goods_names)
            existing_goods_dict = {goods.name: goods for goods in existing_goods}

            update_list = []
            new_goods_list = []

            for goods in bazar_goods:
                if goods.name in existing_goods_dict:
                    goods_obj = existing_goods_dict[goods.name]
                    goods_obj.current_quantity += goods.quantity
                    goods_obj.has_purchased = False
                else:
                    goods_obj = Goods(
                                    name=goods.name, 
                                    goods_type=goods.goods_type, 
                                    current_quantity=goods.quantity,
                                    measurement_type=goods.measurement_type,
                                )
                    new_goods_list.append(goods_obj)
                update_list.append(goods_obj)
            
            with transaction.atomic():
                Goods.objects.bulk_create(new_goods_list)
                Goods.objects.bulk_update(update_list, ["current_quantity", "has_purchased"])
            
            bazar_obj.added_with_goods_list = True
            bazar_obj.save()
            return Response({"message": "Successfully Good list updated"}, status=200)
        
        return Response({"message": "Already has been updated"}, status=400)

