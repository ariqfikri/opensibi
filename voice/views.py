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
    file3d = request.GET.get('file')
    query = "SELECT nama_file FROM voice WHERE input_kata like '%"+ file3d +"%'"
    with connection.cursor() as cursor:
        cursor.execute(query)
        # return Response.ok(BASE_DIR, message="Success")
        # return Response.ok(cursor.fetchone(), message="Success")
        t = TemplateResponse(request, 'index.html', {})
        return HttpResponse(t.render())
        template = loader.get_template("")
        return HttpResponse(template.render)
