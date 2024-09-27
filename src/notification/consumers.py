from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

from notification.models import Notification
User = get_user_model()


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.notification_room = None


        shopper_id = self.scope["query_params"]["shopper_id"][0]
        
        # Make a new individual channel for user for chat related global data sending
        try:
            shopper = await sync_to_async(User.objects.get)(id=shopper_id)
            self.notification_room = f"notification_room_{shopper.id}"
            await self.channel_layer.group_add(self.notification_room, self.channel_name)

            total_unread_notification = await sync_to_async((Notification.objects.filter)(user_obj=shopper, has_read=False).count)()
            # Sends unread message count and room info to receiver through notification consumer.
            await self.send_json(
                {
                    'type': 'message_notification',
                    "response_type": "initial_msg_notification",
                    "total_unread_notification": total_unread_notification,
                }
            )
            
        except:
            pass

    async def receive_json(self, content) -> None:
        # Receive payload from client side
        pass

    async def disconnect(self, close_code) -> None:
        if self.notification_room:
            await self.channel_layer.group_discard(self.notification_room, self.channel_name)

    async def message_notification(self, event) -> None:
        # Send messages to a respective layer
        await self.send_json(event)
