from .models import Carts, Items
import requests
import sys
import logging
logger = logging.getLogger(__name__)

def validate_order(cart):
    """
      Should send a request to validate the order based on endpoint
    """
    return 'Request Sent for user %s' % cart['user_id']

def cart_checkout(cart, callback=validate_order):
    """
      Receiving carts to save into Database
    """
    try:
      Carts.objects.create(
        cart_id = cart['id'],
        user_id = cart['user_id'],
        subtotal = cart['subtotal'],
        shipping_cost = cart['shipping_cost']
      ).save()
      
      temp_list = []
      for item in cart['item_list']:
        item = Items(
          cart_id = cart['id'],
          item_id = item['id'],
          item_price = item['item_price'],
          quantity = item['quantity'],
          shipping_cost = item['shipping_cost']
        )
        temp_list.append(item)
        
      Items.objects.bulk_create(temp_list)

      callback(cart)
      return "Checkout for user %s" % cart['user_id']

    except:
      print('Un-expected Error in saving, issue was %s' % sys.exc_info()[0])
      logger.error(sys.exc_info()[1])
      raise

