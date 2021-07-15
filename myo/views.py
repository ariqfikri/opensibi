import numpy as np
import pickle
from opensibi.response import Response
from opensibi.middleware import *
from project.models import Token
from monitor.models import Log
from opensibi.normalization import minmax
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@jwtRequired
@csrf_exempt
def myo(request):
  getToken = request.META['HTTP_AUTHORIZATION']
  decodeToken = decode(getToken)
  getToken = str(getToken).split(' ')
  cek = list(decodeToken.values())
  token = Token.objects.filter(token_user=getToken[1]).first()
  if cek[2] == 'myo':
    if token.status == 'unused':
      token.ip = request.META.get('REMOTE_ADDR')
      token.status = 'used'
      token.save()
    else:
      with open('model/model.sav', 'rb') as handle:
        loaded_model = pickle.load(handle)
      test_data = request.POST.get('test')
      test_data = test_data.split(';')
      test_data = np.array(test_data)
      test_data = minmax(test_data)
      predict = loaded_model.predict(test_data)
      predict = predict.tolist()
      log = Log()
      log.name = "Myo Service"
      log.status = "success"
      log.method = "Post"
      log.save()
      return Response.ok(predict, message="Success")
  else:
    return Response.unauthorized(message="unauthorized")
    
    