from sklearn.neighbors import KNeighborsClassifier
from django.db import connection
import numpy as np
import pickle
from opensibi.response import Response
from opensibi.middleware import jwtRequired
from monitor.models import Log
from project.models import *
from opensibi.middleware import *
from opensibi.normalization import minmax
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.template import Context, loader
from django.template.response import TemplateResponse

@jwtRequired
@csrf_exempt
def voice(request):
  getToken = request.META['HTTP_AUTHORIZATION']
  decodeToken = decode(getToken)
  getToken = str(getToken).split(' ')
  cek = list(decodeToken.values())
  token = Token.objects.filter(token_user=getToken[1]).first()
  if cek[2] == 'voice':
    if token.status == 'unused':
      token.ip = request.META.get('REMOTE_ADDR')
      token.status = 'used'
      token.save()
    else:
        filename = request.GET.get('file')
        if len(filename) > 1:
            query = "SELECT nama_file FROM voice WHERE input_kata like '%"+ filename +"%'"
        else:
            query = "SELECT nama_file FROM voice WHERE input_kata = '"+ filename +"'"
        with connection.cursor() as cursor:
            cursor.execute(query)
        # return Response.ok(BASE_DIR, message="Success")
        # return Response.ok(cursor.fetchone()[0], message="Success")
            path = 'file/'+cursor.fetchone()[0]
        # return path
            log = Log()
            log.name = "Voice Service"
            log.status = "success"
            log.method = "Post"
            log.save()
            t = TemplateResponse(request, 'index.html', {'daepath': path})
            return HttpResponse(t.render())
  else:
    return Response.unauthorized(message="unauthorized")
    
