from .models import Carts
import requests


def validate_order(self, cart):
    """
      Should send a request to validate the order based on endpoint
    """
    print(cart)

def cart_checkout(self, cart, callback=validate_order):
    """
      Receiving carts to save into Database
    """
    Carts.objects.create({
      cart_id : cart.id,
      user_id : cart.user_id,
      subtotal : cart.subtotal,
      shipping_cost : cart.shipping_cost
    }).save()

    for item in cart.item_list:
      Items.objects.create({
        cart_id : cart.cart.id,
        item_id : item.id,
        item_price : item.item_price,
        quantity : item.quantity
    }).save()

    callback(cart)
    return 'Checkout for user %s' % cart.user_id

