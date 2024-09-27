from rest_framework import serializers
from django.conf import settings
from inventory.models import Goods


class GoodsSerializer(serializers.ModelSerializer):
    measure_of = serializers.SerializerMethodField()
    goods_type_display = serializers.SerializerMethodField()
    goods_icon = serializers.SerializerMethodField()

    class Meta:
        model = Goods
        fields = (
            "id",
            "icon",
            "goods_icon",
            "name",
            "goods_type",
            "goods_type_display",
            "standard_quantity",
            "current_quantity",
            "measurement_type",
            "is_one_time",
            "has_purchased",
            "measure_of",
            "created_at",
            "updated_at",
        )

        extra_kwargs = {
            "name": {"required": True, "allow_null": False},
            "goods_type": {"required": True, "allow_null": False},
            "standard_quantity": {"required": True, "allow_null": False},
            "current_quantity": {"required": True, "allow_null": False},
            "measurement_type": {"required": True, "allow_null": False},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # call the super()

        # Set 'required' attribute for icon field based on context
        context = kwargs.get("context", {})
        is_creating = context.get("is_creating", False)

        if is_creating:
            self.fields["icon"].required = True
        else:
            self.fields["icon"].required = False
            self.fields["icon"].allow_null = True  # Allow null for updates

        for field in self.fields:  # iterate over the serializer fields
            self.fields[field].error_messages["required"] = (
                "%s field is required"
                % field.replace("_obj", " ").replace("_", " ").upper()
            )  # set the custom error message
            self.fields[field].error_messages["invalid"] = (
                "%s is not valid" % field.replace("_obj", " ").replace("_", " ").upper()
            )
            self.fields[field].error_messages["blank"] = (
                "%s field is blank"
                % field.replace("_obj", " ").replace("_", " ").upper()
            )

    def get_measure_of(self, obj):
        if obj.measurement_type:
            return obj.measurement_type
        return "-"
    
    def get_goods_type_display(self, obj):
        if obj.goods_type:
            return obj.get_goods_type_display()
        return "-"
    
    def get_goods_icon(self, obj):
        if obj.icon:
            return f"{settings.BACKEND_SERVICE_HOST}{settings.MEDIA_URL}{obj.icon}"
        return ""
