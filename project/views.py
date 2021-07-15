from monitor.transformer import transform
from sklearn.neighbors import KNeighborsClassifier
from django.db import connection
import numpy as np
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from user.models import Users
from project.forms import formUsers,formProject
from opensibi.response import Response
from opensibi.middleware import *
from project.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from project import transformer


@csrf_exempt
def projects(request):
    project = Project()
    project.project_name = request.POST.get('project_name')
    project.id_user_id = request.session['user_id']
    project.save()
    return redirect("/")


@csrf_exempt
def getToken(request, id):
    project = Project.objects.filter(id=id).first()
    project = transformer.singleTransform(project)
    jwt = JWTAuth()
    generateToken = jwt.encode({"id": project['id'], "id_user": project['id_user'], "project_name": project['project_name']})
    token = Token.objects.filter(token_user=generateToken).first()
    if not token:
        token = Token()
        token.token_user = generateToken
        token.status = "unused"
        token.save()
    else:
        return Response.ok(generateToken, message='token already generated')
    return Response.ok(generateToken, message="Success")


@csrf_exempt 
def loginUser(request):
    form = formUsers()
    if request.method == 'POST':
        m = Users.objects.filter(email=request.POST['email']).first()
        print("if 1")
    if not m:
        return render(request, "loginUser.html", {'warning': "e-mail not registered ", 'form': form})
    if m.password == request.POST['password']:
        print("masuk if2")
        request.session['user_id'] = m.id
        return redirect("/")
    else:
        return render(request, "loginUser.html", {'warning': "password didn't match.", 'form': form})

@csrf_exempt 
def register(request):
    user = Users()
    users = formUsers()
    m = Users.objects.filter(email=request.POST['email'])

    if m:
        return render(request, "register.html", {'warning': "E-mail already registered", 'form': users})
    
    else:
        user = Users()
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.save()
        return render(request, "login.html", {'warning1': "registered successfully", 'form': users})

@csrf_exempt 
def registerUser(request):
    user = Users()
    users = formUsers()
    m = Users.objects.filter(email=request.POST['email'])
    if m:
        return render(request, "registerUser.html", {'warning': "E-mail already registered", 'form': users})
    else:
        user = Users()
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.save()
        return render(request, "loginUser.html", {'warning1': "registered successfully", 'form': users})

@csrf_exempt 
def viewLogin(request):
    users = formUsers()
    return render(request, 'login.html', {'form': users})

@csrf_exempt 
def viewLoginUser(request):
    users = formUsers()
    return render(request, 'loginUser.html', {'form': users})

@csrf_exempt 
def viewRegister(request):
    users = formUsers()
    return render(request, 'register.html', {'form': users})

@csrf_exempt 
def viewRegisterUser(request):
    users = formUsers()
    return render(request, 'registerUser.html', {'form': users})

@csrf_exempt
def viewLogout(request):
    users = formUsers() 
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect("/viewLogin")

@csrf_exempt
def viewLogoutUser(request):
    users = formUsers() 
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return redirect("/viewLoginUser")

@csrf_exempt
def index(request):
    if 'user_id' not in request.session:
        return redirect("/viewLogin")


    users = Users.objects.all()
    totalUser = Users.objects.all().count()
    leap = Project.objects.filter(project_name='leap').count()
    dataLeap = Project.objects.filter(project_name='leap').select_related('id_user')
    dataMyo = Project.objects.filter(project_name='myo').select_related('id_user')
    dataVoice = Project.objects.filter(project_name='voice').select_related('id_user')
    myo = Project.objects.filter(project_name='myo').count()
    voice = Project.objects.filter(project_name='voice').count()
    return render(request, 'dashboard.html', {
                                              'users': users, 
                                              'myo': myo, 
                                              'leap': leap, 
                                              'voice': voice, 
                                              'total': totalUser, 
                                              'dataleaps': dataLeap,
                                              'datamyos': dataMyo,
                                              'datavoices': dataVoice })
@csrf_exempt
def dashboardUser(request):
    if 'user_id' not in request.session:
        return redirect("/viewLoginUser")

    form = formProject()
    project = Project.objects.filter(id_user_id=request.session['user_id'])   
    return render(request, 'dashboardUser.html', {'projects': project, 'form': form})

@csrf_exempt
def test(request):
    project = Project.objects.filter(project_name='leap')
    project = transformer.transform(project)
    return Response.ok(project, message='token already generated')
    
    
