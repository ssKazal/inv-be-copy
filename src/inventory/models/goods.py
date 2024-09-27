import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from inventory.custom.general_func import generate_uids


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)
User = get_user_model()


# Create your models here.
class Goods(models.Model):
    def _upload_to(self, filename):
        """
        Creating a specific folder for saving file to make find easily.
        """
        uid = generate_uids()  # Generating random string value
        now_time = datetime.datetime.now()
        return (
            "Goods/id-"
            + uid
            + "/"
            + str(now_time.strftime("%Y-%m-%d"))
            + "/"
            + filename
        )
    
    _GOODS_TYPE_CHOICES = (
        ("cooking", "Cooking"),
        ("snacks", "Snacks"),
        ("household", "Household"),
    )

    icon = models.ImageField(max_length=256, upload_to=_upload_to, null=True)
    name = models.CharField(max_length=100, null=True, unique=True)
    goods_type = models.CharField(max_length=25, choices=_GOODS_TYPE_CHOICES, null=True)
    standard_quantity = models.DecimalField(
        default=0.00,
        validators=[MinValueValidator(0.00)],
        decimal_places=2,
        max_digits=15,
        null=True,
    )
    current_quantity = models.DecimalField(
        default=0.00,
        validators=[MinValueValidator(0.00)],
        decimal_places=2,
        max_digits=15,
        null=True,
    )
    measurement_type = models.CharField(max_length=10, null=True)
    is_one_time = models.BooleanField(default=False)
    has_purchased = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    __icon = None
    __name = None
    __standard_quantity = None
    __current_quantity = None
    __measurement_type = None
    __is_one_time = None

    class Meta:
        verbose_name_plural = "Goods"

    def __init__(self, *args, **kwargs):
        super(Goods, self).__init__(*args, **kwargs)
        self.__icon = self.icon
        self.__name = self.name
        self.__standard_quantity = self.standard_quantity
        self.__current_quantity = self.current_quantity
        self.__measurement_type = self.measurement_type
        self.__is_one_time = self.is_one_time

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        goods_obj = super().save(*args, **kwargs)
        cache.delete("goods_qs")
        cache.set("goods_qs", Goods.objects.all().order_by("-id"), timeout=CACHE_TTL)

        return goods_obj
