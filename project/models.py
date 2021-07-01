from django.db import models
from datetime import datetime
from user.models import Users

class Project(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default=datetime.utcnow)
    updated_at = models.DateTimeField(default=datetime.utcnow)

    class Meta:
        db_table = 'project'