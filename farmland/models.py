from django.db import models
from django.conf import settings  # ✅ Import settings instead of using auth.User

class Farmland(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="farmland")  
    crop_type = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    land_area = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.crop_type}"


