from django.db import models

# Create your models here.
class TimeStamp(models.Model):
    id: int
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True