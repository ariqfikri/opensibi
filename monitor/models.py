from datetime import datetime
from django.db import models


# Create your models here.
class Log(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, null=True)
    method = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=230, null=False)
    created_at = models.DateTimeField(default=datetime.now)
    class Meta:
        db_table = 'logs'
