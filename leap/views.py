from django.db import connection
from opensibi.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from opensibi.middleware import jwtRequired
from monitor.models import Log
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
import os
import numpy as np

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

@csrf_exempt
def leap(request):
    new_model =  load_model('alphasibi-14.6.h5')
    data = request.POST.get('test').split(',')
    get = request.POST.get('get')

    data = np.array(data).astype(float)
    data = np.expand_dims(data, axis=0)
    result = new_model.predict(data)
    result = getLabel(result[0])
    result = sort(result, get)
    return Response.ok(result, message="Success")


def getLabel(testLabel):
  label = ['None', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P','Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  result = {}
  for index, l in enumerate(label):
    result[l] = float("{:.2f}".format(testLabel[index]))
  return result
 
def sort(data, get=None):
  sortedData = (sorted(data.items(), key=lambda x:x[1], reverse=True))
  sortedData = [list(elem) for elem in sortedData]
  sortedData = [x for x in sortedData if x[1] > 0]
  if get!=None:
    if int(get)==0:
      sortedData = sortedData[0][0]
    else:
      sortedData = sortedData[:int(get)]
  return sortedData