from django.shortcuts import render
from monitor.models import Log
from monitor import transformer
from opensibi.response import Response
# Create your views here.
def monitor(request):
  log = Log.objects.all()
  log = transformer.transform(log)
  return Response.ok(values=log)

