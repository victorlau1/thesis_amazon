from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from .models import Carts, Items
from .serializers import CartSerializer, ItemSerializer
from .services import cart_checkout
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def cart_detail(request):
  """
   Routes to cat checkout services
  """

  if request.method == 'GET':
    
    carts = Carts.objects.all()
    serializer = CartSerializer(carts, many=True)
    return JsonResponse(serializer.data, safe=False)

  elif request.method == 'POST': 
    data = JSONParser().parse(request)
    try:
      cart_checkout(data)
      return JsonResponse('Posted', status=201, safe=False)
    except:
      return JsonResponse('Error Saving Data', status=400, safe=False)


