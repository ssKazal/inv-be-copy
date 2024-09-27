from django.contrib import admin
from inventory.models import Goods, GoodsLog, Bazar, BazarGoods

# Register your models here.
admin.site.register([Goods, GoodsLog, Bazar, BazarGoods])
