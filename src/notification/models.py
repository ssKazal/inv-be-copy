from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Notification(models.Model):
    text = models.CharField(max_length=1000, null=True)
    user_obj = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    has_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.text
