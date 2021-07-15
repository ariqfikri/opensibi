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
import joblib 
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd


scaler = MinMaxScaler()
df = pd.read_csv('myo.csv', header=None)
X = df.loc[:, df.columns != 0]
y = df[0]

# Create KNN classifier
knn = KNeighborsClassifier(algorithm ='auto', leaf_size= 1, metric= 'minkowski',n_neighbors= 1, p = 2, weights= 'uniform')
X = scaler.fit_transform(X)
knn.fit(X,y)

@csrf_exempt
def myo(request):
  if request.method == 'POST':
    # model = joblib.load('myo.pkl')
    # scaler = joblib.load('scaler.pkl')
    # assert isinstance(scaler, MinMaxScaler)
    test_data = request.POST.get('test')
    test_data = test_data.split(',')
    test_data = np.array(test_data)
    test_data = np.expand_dims(test_data, axis=0)
    test_data = scaler.transform(test_data)
    predict = knn.predict(test_data)
    predict = predict.tolist()
  return Response.ok(predict[0], message="Success")