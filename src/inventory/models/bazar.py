from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from inventory.models.goods import Goods
from notification.models import Notification
from inventory.custom.general_func import send_notification

User = get_user_model()


class Bazar(models.Model):
    BAZAR_STATUS = (
        ("created", "Created"),
        ("started", "Started"),
        ("end", "End"),
        ("done", "Done"),
    )
    shopper = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bazar_date = models.DateField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=100, choices=BAZAR_STATUS, default="created")
    added_with_goods_list = models.BooleanField(default=False)  # To check if the bazar goods added to the goods list or not
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)

class BazarGoods(models.Model):
    bazar_obj = models.ForeignKey(Bazar, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=True)
    goods_type = models.CharField(max_length=25, choices=Goods._GOODS_TYPE_CHOICES, null=True)
    quantity = models.DecimalField(
        default=0.00,
        validators=[MinValueValidator(0.00)],
        decimal_places=2,
        max_digits=15,
        null=True,
    )
    measurement_type = models.CharField(max_length=10, null=True)
    price = models.DecimalField(
        default=0.00,
        validators=[MinValueValidator(0.00)],
        decimal_places=2,
        max_digits=15,
        null=True,
    )
    is_one_time = models.BooleanField(default=False)
    has_purchased = models.BooleanField(default=False)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('bazar_obj', 'name',)

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):

        # If other user except shopper add bazar goods, we will alert
        # shopper by sending realtime notification
        if not self.id:
            if self.added_by != self.bazar_obj.shopper:
                Notification.objects.create(text=f"{self.added_by.username} has added {self.name} to the bazar list", user_obj=self.bazar_obj.shopper)
                send_notification(self.bazar_obj.shopper)

        return super().save(*args, **kwargs)
