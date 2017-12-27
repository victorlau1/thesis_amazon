from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .models import Carts, Items
from .serializers import CartSerializer, ItemSerializer
from .services import cart_checkout

class CartViewSet(viewsets.ModelViewSet):
  """
  API endpoint that handles incoming post requests for carts
  """
  queryset = Carts.objects.all()
  serializer_class = CartSerializer

class InventoryViewSet(viewsets.ModelViewSet):
  """
  API endpoint that handles incoming post requests for validating inventory levels
  """


