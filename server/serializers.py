from rest_framework import serializers
from .models import Carts, Items


class CartSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Carts
    fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):

  class Meta:
    model = Items
    fields = '__all__'



