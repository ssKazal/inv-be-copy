from django.urls import path
from notification.views import notifications

urlpatterns = [
    path("<int:user_id>/", notifications, name="notifications"),
]
