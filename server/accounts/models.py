from django.db import models
from commons.models import TimestampedModel
# Create your models here.


from django.conf import settings
from django.db import models


class UserProfile(TimestampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    full_name = models.CharField(
        max_length=255, 
    )

    user_email = models.EmailField(
        max_length=255,
        unique=True,
    )

    firebase_uid = models.CharField(
        max_length=128,
        unique=True,
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )

    user_phone_number = models.CharField(
        max_length=13,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username


class UserAuthProvider(TimestampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="auth_providers",
    )

    provider_name = models.CharField(
        max_length=50,
    )

    provider_id = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return f"{self.user.username} - {self.provider_name}"


