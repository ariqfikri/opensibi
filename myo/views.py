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


@csrf_exempt
def myo(request):
  if request.method == 'POST':
    with open('model.sav', 'rb') as handle:
        loaded_model = pickle.load(handle)
    test_data = request.POST.get('test')
    test_data = test_data.split(',')
    test_data = np.array(test_data)
    test_data = minmax(test_data)
    predict = loaded_model.predict(test_data)
    predict = predict.tolist()
  return Response.ok(predict, message="Success")