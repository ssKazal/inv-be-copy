from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from inventory.models.goods import Goods
User = get_user_model()
CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class GoodsLog(models.Model):
    user_obj = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    goods_obj = models.ForeignKey(Goods, on_delete=models.CASCADE, null=True)
    notes = ArrayField(models.CharField(max_length=2000, null=True), null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.goods_obj.name) if self.goods_obj else str(self.id)

    def save(self, *args, **kwargs):
        log_obj = super().save(*args, **kwargs)
        if self.goods_obj:
            cache.delete(f"goods_log_{self.goods_obj.id}")
            cache.set(
                f"goods_log_{self.goods_obj.id}",
                GoodsLog.objects.filter(goods_obj=self.goods_obj),
                timeout=CACHE_TTL,
            )

        return log_obj
