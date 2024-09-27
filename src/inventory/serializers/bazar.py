from rest_framework import serializers
from inventory.models import Bazar, BazarGoods


class BazarGoodsSerializer(serializers.ModelSerializer):

    class Meta:
        model = BazarGoods
        fields = (
            "id",
            "name",
            "goods_type",
            "quantity",
            "price",
            "measurement_type",
            "has_purchased",
            "added_by",
            "is_one_time",
            "bazar_obj",
        )
        extra_kwargs = {
            'bazar_obj': {'write_only': True},
        }

class BazarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bazar
        fields = ("id", "shopper", "bazar_date", "status", "added_with_goods_list")
