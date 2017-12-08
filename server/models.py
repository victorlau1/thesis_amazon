from django.db import models

from django.utils import timezone

# Create your models here.
class cart_information(models.Model):
  """ Cart Data Received From Clients Microservice
    
  """
  cart_id = models.IntegerField(primary_key=True)
  item_name = models.CharField(max_length=200)
  price = models.IntegerField()
  ordered_at = timezone.now()
  valid_purchase = models.BooleanField(default=False)

  def __str__(self):
    return self
