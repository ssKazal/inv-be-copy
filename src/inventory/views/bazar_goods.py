from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from inventory.serializers import BazarGoodsSerializer
from inventory.models import BazarGoods
from inventory.permissions import GoodsPermission


class BazarGoodsViewset(viewsets.ModelViewSet):
    serializer_class = BazarGoodsSerializer
    # permission_classes = [GoodsPermission]
    queryset = BazarGoods.objects.all().order_by("-created_at")
