from user.models import Users
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = Users
    fields = ['id', 'name', 'email', 'password', 'created_at', 'updated_at']