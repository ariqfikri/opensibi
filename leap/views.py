from django.db import connection
from opensibi.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from opensibi.middleware import jwtRequired
from monitor.models import Log
from django.views.decorators.csrf import csrf_exempt
from tensorflow.keras.models import load_model
import joblib 
import os
import numpy as np

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
num_features = 69
@csrf_exempt
def leap(request):
  data = request.POST.get('test').split(',')
  get = request.POST.get('get')
  knn = request.POST.get('knn')
  number = request.POST.get('number')

  data = np.array(data).astype(float)
  
  if len(data)==num_features :
    if knn:
      result = 'knn'
      # result = predictKnn(data, get)
    elif number:
      # result = 'number'
      result = predictNumber(data, get)
    else:
      result = 'abjad'
      result = predictOne(data, get)
  else:
    result = predictMany(data, get)
  return Response.ok(result, message="Success")

def predictMany(data, get):
  manyData = []
  start = 0
  for end in range(num_features,len(data),num_features):
    # manyData.append(data[start:end])
    manyData.append(predictOne(data[start:end], get))
    start = end
  return manyData

def predictOne(data, get):
  model =  load_model('model/alphasibi-14.6.h5')
  data = np.expand_dims(data, axis=0)
  result = model.predict(data)
  result = getLabel(result[0])
  result = sort(result, get)
  return result

def predictNumber(data, get):
  model = load_model('model/alphasibi-angka.h5')
  data = np.expand_dims(data, axis=0)
  result = model.predict(data)
  result = getLabel(result[0],number=True)
  result = sort(result, get)
  return result

def predictKnn(data, get):
  model = joblib.load('model/knn.pkl')
  data = np.expand_dims(data, axis=0)
  result = model.predict(data)
  result = getLabel(result[0])
  result = sort(result, get)
  return result


def getLabel(testLabel,number=False):
  labelAbjad = ['None', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P','Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
  labelNumber = [1,2,3,4,5,6,7,8,9]
  labelNumber = [str(x) for x in labelNumber]

  label = labelNumber if number else labelAbjad

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