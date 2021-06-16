from sklearn.neighbors import KNeighborsClassifier
from django.db import connection
import numpy as np
import pickle
from opensibi.response import Response
from opensibi.middleware import jwtRequired
from monitor.models import Log
from opensibi.normalization import minmax
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.template import Context, loader
from django.template.response import TemplateResponse

@csrf_exempt
def voice(request):
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
        t = TemplateResponse(request, 'index.html', {'daepath': path})
        return HttpResponse(t.render())
