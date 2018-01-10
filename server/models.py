from django.db import models
from django.utils import timezone


class Carts(models.Model):
  """ 
    Cart Data Received From Clients Microservice
  """
  cart_id = models.IntegerField(primary_key=True)
  user_id = models.IntegerField()
  subtotal = models.FloatField()
  shipping_cost = models.FloatField()
  ordered_at = timezone.now()

  def __str__(self):
    return {(field.name, field.value_to_string(self)) for field in Carts._meta.fields}

  
class Items(models.Model):
  """
    Item per Cart list; Combo Key is cart_id, and item_id. 
  """
  class Meta:
    unique_together = ('cart','item_id')
  item_id = models.IntegerField()
  cart = models.ForeignKey(Carts, db_constraint=False, on_delete=models.CASCADE)
  item_price = models.FloatField()
  shipping_cost = models.FloatField()
  quantity = models.IntegerField()
  valid_purchase = models.BooleanField(default=False)
