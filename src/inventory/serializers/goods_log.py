from rest_framework import serializers
from inventory.models import GoodsLog

class GoodsLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsLog
        fields = ("id", "user_obj", "goods_obj", "notes", "created_at")

        extra_kwargs = {
            "user_obj": {"required": True, "allow_null": False},
            "goods_obj": {"required": True, "allow_null": False},
        }

