# import necessary libraries
import random
import string
from django.db import models
from django.utils import timezone
from datetime import timedelta

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    accessed_at = models.DateTimeField(auto_now_add=True)

class ShortURL(models.Model):
    original_url = models.URLField(unique=True)
    short_key = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_key} -> {self.original_url}"

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField()
    blocked_until = models.DateTimeField()

    def is_blocked(self):
        return self.blocked_until > timezone.now()
