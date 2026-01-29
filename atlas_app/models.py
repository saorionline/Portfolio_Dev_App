from django.db import models

# Create your models here.

class AtlasBaseModel(models.Model):
    """
    Common fields used across most tables.
    """
    title = models.CharField(max_length=200)
    last_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True  # <--- CRITICAL: This tells Django NOT to create a table for this class.