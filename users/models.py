# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class User(AbstractUser):  # ✅ Custom user model extending AbstractUser
#     phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
#     address = models.TextField(null=True, blank=True)
#     district = models.CharField(max_length=100, null=True, blank=True)

#     def __str__(self):
#         return self.username





from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):  # ✅ Custom user model extending AbstractUser
    ROLE_CHOICES = [
        ('farmer', 'Farmer'),
        ('seller', 'Seller'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='farmer')

    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
