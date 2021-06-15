from django.db import connection
from opensibi.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from opensibi.middleware import jwtRequired
from monitor.models import Log
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model

@csrf_exempt
def leap(request):
    new_model =  load_model('alphasibi-14.6.h5', compile = False)
    test_data = request.POST.get('test')
    new_model.predict(test_data)
    return Response.ok(values="ff", message="Success")

 