import pandas as pd
import numpy as np
from django.db import connection

def minmax(test_data):
  with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM max")
    max = cursor.fetchall()
    cursor.execute("SELECT * FROM min")
    min = cursor.fetchall()

  max = pd.DataFrame(max)
  min = pd.DataFrame(min)
  test_data = [float(i) for i in test_data]
  test_data = pd.DataFrame(test_data)
  test_data = (test_data-min)*(1-0)/(max-min)
  test_data = np.array(test_data)
  test_data = test_data.reshape(1,-1)

  return test_data