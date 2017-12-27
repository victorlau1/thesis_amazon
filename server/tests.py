from django.test import TestCase
from unittest.mock import MagicMock
from .models import Carts, Items
from .services import validate_order, cart_checkout
from .serializers import CartSerializer
from django.urls import reverse
from rest_framework.test import APIRequestFactory, APITestCase

### Model Tests

class Cart_Models_Tests(TestCase):
  """
    Cart Model Tests that cover Model Creation
  """

  def create_test_cart(self, cart_id=15, user_id=20, subtotal=79.99, shipping_cost=13.05):
    """
      Test Object for Testing
    """
    item_list = [{
          'id': 49200,
          'shipping_cost': 9.86,
          'item_price': 99.99,
          'valid_purchase': False,
          'quantity': 3
          },
          {
          'id': 49100,
          'shipping_cost': 5.00,
          'item_price': 39.99,
          'valid_purchase': False,
          'quantity': 2
          }]

    return Carts.objects.create(cart_id=cart_id, user_id=user_id, subtotal=subtotal, shipping_cost=shipping_cost)
  
  def test_create_cart(self):
    """
      Check model is the same as expected
    """

    test_cart = self.create_test_cart()
    self.assertTrue(isinstance(test_cart, Carts))
    self.assertEqual(test_cart.cart_id, 15)
    self.assertEqual(test_cart.user_id, 20)
    self.assertEqual(test_cart.subtotal, 79.99)
    self.assertTrue(test_cart.ordered_at)
    print('Cart Creation Works')

class Item_Models_Tests(TestCase):
  """
    Item Insertion and Foreign Key Relationship with Carts
  """

  def setUp(self):
    """
      Test Object for Testing
    """

    self.cart = {
      'id': 49100,
      'user_id': 23,
      'shipping_cost': 7.60,
      'subtotal': 148.00,
      'item_list': [{
            'id': 49200,
            'shipping_cost': 9.86,
            'item_price': 100.00,
            'valid_purchase': False,
            'quantity': 3
            },
            {
            'id': 49100,
            'shipping_cost': 5.00,
            'item_price': 40.00,
            'valid_purchase': False,
            'quantity': 2
            }]
      }

  def test_item_inserted(self):
    """
      Each item will save appropriately within the database table
    """
    test_cart = self.cart
    for item in test_cart:
      Items.objects.create({
        cart_id : test_cart.cart_id,
        id : item.id,
        item_price : item.item_price,
        shipping_cost : item.shipping_cost,
        quantity : item.quantity
      }).save()
    self.assertEqual(Items.objects.count(), 2)
    print('All Items saved')

### Database Models Test

class Cart_Database_Tests(TestCase):
  """
    Cart DB Model Test Checks
  """

  def test_save_cart(self):
    """
      Cart is saved correctly to DB
    """
    test_cart = Cart_Models_Tests.create_test_cart(self)
    test_cart.save()
    test_cart_db = Carts.objects.filter(pk=test_cart.cart_id)
    self.assertEqual(test_cart_db[0].cart_id, test_cart.cart_id)
    print('Cart Save Works')
  

class Item_Database_Tests(TestCase):
  """
    Item DB Model Test Checks 
  """
  def test_item_purchase(self):
    """
      Cart Model Updates Appropriately When Receiving 
    """
    test_cart = Cart_Models_Tests.create_test_cart(self)
    for item in test_cart.item_list:
      Items.objects.create({
        cart_id : test_cart.cart_id,
        id : item.id,
        item_price : item.item_price,
        shipping_cost : item.shipping_cost,
        quantity : item.quantity
      }).save()
    self.assertEqual(Items.objects.get(id=item.id, cart_id=test_cart.cart_id).valid_purchase, False)
    Items.objects.get(id=item.id, cart_id=test_cart.cart_id).update(valid_purchase=True)
    self.assertEqual(Items.objects.get(id=item.id, cart_id=test_cart.cart_id).valid_purchase, True)
    print('Updated Purchase from False to True')


###Services API ACTIONS

class Cart_Services_Test(TestCase):

  def setUp(self):
       
      self.test_data = {
      'cart_id': 100,
      'item_list': [{
          'id': 49200,
          'shipping_cost': 9.86,
          'item_price': 99.99,
          'valid_purchase': False,
          'quantity': 3
          },
          {
          'id': 49100,
          'shipping_cost': 5.00,
          'item_price': 39.99,
          'valid_purchase': False,
          'quantity': 2
          }],
      'user_id': 25
    }

  #def cart_checkout(self, test_data, callback=MockTest.):



###REST API ACTIONS

class Cart_API_Tests(APITestCase):
  """
    Cart API Endpoints Include:
      1. POST /purchases - Receives purchases that have been checked out
      2. PATCH /purchases/valid - Receive purchases that have been validated
      3. PATCH /purchases/cancel - Cancel Orders (Not Implemented)
  """

  def setUp(self):
    """
      Setup data for all cart tests
    """

    self.test_data = {
      'cart_id': 100,
      'user_id': 25,
      'item_list': [{
          'id': 49200,
          'shipping_cost': 9.86,
          'item_price': 99.99,
          'valid_purchase': False,
          'quantity': 3
          },
          {
          'id': 49100,
          'shipping_cost': 5.00,
          'item_price': 39.99,
          'valid_purchase': False,
          'quantity': 2
          }]
    }

    self.test_data2 = {
      'cart_id': 120,
      'user_id': 35,
      'item_list': [{
          'id': 49600,
          'shipping_cost': 10.00,
          'item_price': 340.00,
          'valid_purchase': False,
          'quantity': 3
          },
          {
          'id': 49400,
          'shipping_cost': 15.00,
          'item_price': 60.00,
          'valid_purchase': False,
          'quantity': 2
          }]
    }

    self.purchase_fail = {
      'valid_purchase': False
    }

    self.purchase_success = {
      'valid_purchase': True
    }
  
  def purchase_already_processing(self):
    """
      GET Request 
      If cart is already in process of being verified, do not send another request
    """
    url = reverse("/purchases/")
    response = self.client.post(url, self.test_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    self.assertEqual(response.body.message, 'Order Already Placed')

  def create_cart_insertion(self):
    """
      Should check that the model is created from the API endpoint
    """
    url = reverse("/purchases/")
    response = self.client.post(url, self.test_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Carts.objects.count(), 1)
    self.client.post(url, self.test_data2, format='json')
    self.assertEqual(Carts.objects.count(), 2)
    print('Cart Insertion Correctly')

  def request_stock_verification(self):
    """
      Should send a get request to external inventory when receives cart information
    """
    url = reverse("/purchases")
    response = self.client.post(url, self.test_data, format='json')
    
    print('Request is sent for stock verification')


  def order_placed(self):
    """
      Should send a response to client that order has been placed once received.
    """
    response = self.client.post('/purchases', self.test_data)
    self.assertEqual(response.message, 'Order Saved')

  def verify_valid_purchase(self):
    """
      Should validate purchase based on information received.
      Send response that purchase is not valid if received from server is false.
    """
  #Should send a request back to cart information about invalid request

  #Cart Model should send back to client if valid_purchase is false
 
  #Cart Model should send copy to delivery service





