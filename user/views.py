from django.shortcuts import redirect, render
from user.models import Users
from user.serializers import UserSerializer
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from project.forms import *
from opensibi.middleware import *
from django.contrib.auth.hashers import check_password
from opensibi.response import Response
from user import transformer
from project.views import index
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from monitor.models import Log

class UserViewset(viewsets.ModelViewSet):
  queryset = Users.objects.all()
  serializer_class = UserSerializer

@csrf_exempt 
def login(request):
    form = formUsers()
    if request.method == 'POST':
        m = Users.objects.filter(email=request.POST['email']).first()
        print("if 1")
    if not m:
        return render(request, "login.html", {'warning': "e-mail not registered ", 'form': form})
    if m.password == request.POST['password']:
        print("masuk if2")
        request.session['user_id'] = m.id
        return redirect("/admin")
    else:
        return render(request, "login.html", {'warning': "password didn't match.", 'form': form})

@csrf_exempt
def logoutApi(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return Response.ok(values="",meesage="Logout successfully")
    
@csrf_exempt 
def auth(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = Users.objects.filter(email=email).first()
        if not user:
            return Response.badRequest(message='e-mail not registered')
        if not (request.POST['password'] == user.password):
            return Response.badRequest(message="e-mail or password didn't match")
        request.session['user_id'] = user.id
        user = transformer.singleTransform(user)
        return Response.ok(values=user, message="login successfully")