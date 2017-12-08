from django.test import TestCase
from ./models import cart_information
from
# Create your tests here.

### Model Tests

class Cart_Information(TestCase):

  #Create a test object
  def create_test_cart(self, cart_id=1, item_name='Dremel Micro',price=79.99,valid_purchase):
    return cart_information.objects.create(cart_id=cart_id,item=item,price=price, valid_purchase=valid_purchase)
  
  #Testing that cart created is the same
  def test_create_cart(self):
    test_cart = self.create_test_cart
    self.assertTrue(isinstance(test_cart, cart_information))
    self.assertEqual(test_cart.item_name, 'Dremel Micro')
    self.assertEqual(test_cart.cart_id, 1)
    self.assertEqual(test_cart.price, 79.99)
    self.assertEqual(test_cart.valid_purchase, False)
    self.assertTrue(isinstance(test_cart.ordered_at, timezone.now()))

#Cart Model should allow for updates to validate purchases
  def update_purchase(self):
    test_cart = self.create_test_cart
    self.assertTrue(test_cart.valid_purchase, False)
    cart_information.objects.filter(pk=test_cart.pk).update(valid_purchase=True)
    self.assertTrue(test_cart.valid_purchase, True)


#REST API ACTIONS

#Cart Model should send back to client if valid_purchase is false

#Cart Model should send copy to delivery service

#Cart Model should send copy to 




### Server Request Test
#

