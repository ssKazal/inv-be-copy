import json
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User
from inventory.custom.custom_middlewares import GetCurrentUserMiddleWare
from inventory.models import Goods, GoodsLog


@receiver(post_save, sender=Goods)
def goods_log(sender, instance, created, **kwargs):
    user_obj = None
    access_token = None
    user_info_url = f"{settings.BACKEND_SERVICE_HOST}/user-info-from-token/"
    thread_local = GetCurrentUserMiddleWare.thread_local

    if hasattr(thread_local, "current_user_token"):
        access_token = thread_local.current_user_token

    response = requests.get(user_info_url, headers={"Authorization": access_token})
    if response:
        user_id = response.json()["id"]
        user_obj = User.objects.get(id=user_id)

    username = "-"
    if user_obj:
        username = user_obj.username

    notes_str = []
    if created:  # since .save() would tirgger signal, and single has log
        notes_str.append(
            json.dumps(
                {
                    "username": username,
                    "name": instance.name,
                    "action_field": None,
                    "action_type": "add",
                    "previous_value": None,
                    "current_value": None,
                    "date": instance.created_at.strftime("%Y-%m-%d, %H:%M %p"),
                }
            )
        )

    else:
        if instance._Goods__icon != instance.icon:
            print(instance.icon.url)
            notes_str.append(
                json.dumps(
                    {
                        "username": username,
                        "name": instance.name,
                        "action_field": "icon",
                        "action_type": "update",
                        "previous_value": f"{settings.BACKEND_SERVICE_HOST + instance._Goods__icon.url}",
                        "current_value": f"{settings.BACKEND_SERVICE_HOST + instance.icon.url}",
                        "date": instance.updated_at.strftime("%Y-%m-%d, %H:%M %p"),
                    }
                )
            )
        if instance._Goods__name != instance.name:
            notes_str.append(
                json.dumps(
                    {
                        "username": username,
                        "name": instance.name,
                        "action_field": "name",
                        "action_type": "update",
                        "previous_value": instance._Goods__name,
                        "current_value": instance.name,
                        "date": instance.updated_at.strftime("%Y-%m-%d, %H:%M %p"),
                    }
                )
            )
        if instance._Goods__standard_quantity != instance.standard_quantity:
            notes_str.append(
                json.dumps(
                    {
                        "username": username,
                        "name": instance.name,
                        "action_field": "standard_quantity",
                        "action_type": "update",
                        "previous_value": str(instance._Goods__standard_quantity),
                        "current_value": str(instance.standard_quantity),
                        "date": instance.updated_at.strftime("%Y-%m-%d, %H:%M %p"),
                    }
                )
            )
        if instance._Goods__current_quantity != instance.current_quantity:
            notes_str.append(
                json.dumps(
                    {
                        "username": username,
                        "name": instance.name,
                        "action_field": "current_quantity",
                        "action_type": "update",
                        "previous_value": str(instance._Goods__current_quantity),
                        "current_value": str(instance.current_quantity),
                        "date": instance.updated_at.strftime("%Y-%m-%d, %H:%M %p"),
                    }
                )
            )

        if instance._Goods__measurement_type != instance.measurement_type:
            notes_str.append(
                json.dumps(
                    {
                        "username": username,
                        "name": instance.name,
                        "action_field": "measurement_type",
                        "action_type": "update",
                        "previous_value": instance._Goods__measurement_type,
                        "current_value": instance.measurement_type,
                        "date": instance.updated_at.strftime("%Y-%m-%d, %H:%M %p"),
                    }
                )
            )
        if instance._Goods__is_one_time != instance.is_one_time:
            notes_str.append(
                json.dumps(
                    {
                        "username": username,
                        "name": instance.name,
                        "action_field": "is_one_time",
                        "action_type": "update",
                        "previous_value": "true"
                        if instance._Goods__is_one_time
                        else "false",
                        "current_value": "true" if instance.is_one_time else "false",
                        "date": instance.updated_at.strftime("%Y-%m-%d, %H:%M %p"),
                    }
                )
            )

    if len(notes_str) > 0:
        if user_obj:
            GoodsLog.objects.create(
                user_obj=user_obj, goods_obj=instance, notes=notes_str
            )
        else:
            GoodsLog.objects.create(goods_obj=instance, notes=notes_str)
