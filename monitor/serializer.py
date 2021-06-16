from monitor.models import Log
from rest_framework import serializers

class LogSerializer(serializers.ModelSerializer):
  class Meta:
    model = Log
    fields = ['id', 'name', 'method', 'status', 'created_at']