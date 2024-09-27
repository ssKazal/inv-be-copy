from django.http import JsonResponse
from notification.models import Notification

def notifications(request, user_id):
    notification_qs = Notification.objects.filter(user_obj__id=user_id)
    notifications = notification_qs.order_by('-id').values_list('text', flat=True)
    notification_list = list(notifications)
    notification_qs.update(has_read=True)
    return JsonResponse({"notification_messages": notification_list})
