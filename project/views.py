from sklearn.neighbors import KNeighborsClassifier
from django.db import connection
import numpy as np
import pickle
from opensibi.response import Response
from opensibi.middleware import *
from project.models import Project
from opensibi.normalization import minmax
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from project import transformer

@jwtRequired
@csrf_exempt
def projects(request):
    idUser = decode(request.META['HTTP_AUTHORIZATION'])
    idUser = list(idUser.values())
    project = Project()
    project.project_name = request.POST.get('project_name')
    project.id_user_id = int(''.join(str(i) for i in idUser))
    project.save()
    return Response.ok(transformer.singleTransform(project), message="Success")

@jwtRequired
@csrf_exempt
def getToken(request):
    idUser = decode(request.META['HTTP_AUTHORIZATION'])
    idUser = list(idUser.values())
    idUser = int(''.join(str(i) for i in idUser))
    project = Project.objects.filter(id_user=idUser).first()
    project = transformer.singleTransform(project)
    jwt = JWTAuth()
    token = jwt.encode({"id": project['id'], "id_user": project['id_user'], "project_name": project['project_name']})
    return Response.ok(token, message="Success")