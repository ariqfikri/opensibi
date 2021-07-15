from django.shortcuts import render
from monitor.models import LogView,Log
from monitor import transformer
from opensibi.response import Response
from django.db.models.functions import Substr, Lower 
from django.http import JsonResponse

# Create your views here.
def monitor(request):
  myoData = LogView.objects.filter(name="Myo Service")
  leapData = LogView.objects.filter(name="Leap Service")
  voiceData = LogView.objects.filter(name="Voice Service")
  myoData = transformer.transformView(myoData)
  leapData = transformer.transformView(leapData)
  voiceData = transformer.transformView(voiceData)
    
  data = {
    'myo': myoData,
    'leap': leapData,
    'voice': voiceData,
  } 
  return JsonResponse(data)

