from django.shortcuts import render
from user.models import Users
from user.serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from opensibi.middleware import *
from django.contrib.auth.hashers import check_password
from opensibi.response import Response
from user import transformer
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from monitor.models import Log

class UserViewset(viewsets.ModelViewSet):
  queryset = Users.objects.all()
  serializer_class = UserSerializer

@csrf_exempt 
def auth(request):
    if request.method == 'POST':
        email = request.POST['email']
        log = Log()
        log.name = "Login"
        log.method = "POST"
        user = Users.objects.filter(email=email).first()
        if not user:
            return Response.badRequest(message='Pengguna tidak ditemukan!')
        if not (request.POST['password'] == user.password):
            return Response.badRequest(message="Password atau email yang kamu masukkan salah!")
        user = transformer.singleTransform(user)
        if not user:
            log.status = "Error"
        log.status = "Success"
        log.save()
        jwt = JWTAuth()
        user['token'] = jwt.encode({"id": user['id'], "exp": datetime.utcnow() + timedelta(seconds=3600)})
        return Response.ok(values=user, message="Berhasil masuk!")