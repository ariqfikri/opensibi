from rest_framework.decorators import api_view
from sklearn.neighbors import KNeighborsClassifier
from rest_framework.response import Response
from rest_framework import serializers
from django.db import connection
import numpy as np


class MyoSerializer(serializers.Serializer):
    hasil = serializers.CharField(max_length=200)
    

class Myo(object):
    def __init__(self, hasil):
        self.hasil = hasil
        

@api_view()
def myo(request):
  with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM newlabel")
    train_label = cursor.fetchall()
    train_label = np.array(train_label)
    train_label = train_label.ravel()
    cursor.execute("SELECT * FROM newdata")
    train_data = cursor.fetchall()

  knn = KNeighborsClassifier(n_neighbors = 3, weights = 'distance')
  knn.fit(train_data,train_label)
  predict = knn.predict(train_data)
  kirim = Myo(hasil = predict)
  serializer = MyoSerializer(kirim)
  return Response(serializer.data)
# Create your views here.
