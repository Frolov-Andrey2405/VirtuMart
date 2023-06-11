from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image_url = models.URLField(blank=True, null=True)
