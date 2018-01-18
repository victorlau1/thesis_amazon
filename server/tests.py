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
    Carts.objects.create(cart_id=test_cart['id'], user_id=test_cart['user_id'], subtotal=test_cart['subtotal'], shipping_cost=test_cart['shipping_cost'])
    for item in test_cart['item_list']:
      Items.objects.create(
        cart_id = test_cart['id'],
        item_id = item['id'],
        item_price = item['item_price'],
        shipping_cost = item['shipping_cost'],
        quantity = item['quantity']
      ).save()
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
    test_cart_db = Carts.objects.filter(cart_id=test_cart.cart_id)
    self.assertEqual(test_cart_db[0].cart_id, test_cart.cart_id)
    print('Cart Save Works')
  

class Item_Database_Tests(TestCase):
  """
    Item DB Model Test Checks 
  """
  def setUp(self):

    self.cart = {
      "user_id": 46, 
      "id": 2, 
      "shipping_cost": 16.91, 
      "item_list": [
        {
        "item_price": 301.87, 
        "id": 9, 
        "quantity": 5, 
        "shipping_cost": 7.33, 
        "valid_purchase": "False"
        }, 
        {
          "item_price": 251.55, 
          "id": 7, 
          "quantity": 5, 
          "shipping_cost": 9.58, 
          "valid_purchase": "False"}
        ], 
        "subtotal": 2767.1}

  def test_item_purchase(self):
    """
      Cart Model Updates Appropriately When Receiving Validated Item
    """

    test_cart = self.cart
    Carts.objects.create(cart_id=test_cart['id'], user_id=test_cart['user_id'], subtotal=test_cart['subtotal'], shipping_cost=test_cart['shipping_cost'])
    for item in test_cart['item_list']:
      Items.objects.create(
        cart_id = test_cart['id'],
        item_id = item['id'],
        item_price = item['item_price'],
        shipping_cost = item['shipping_cost'],
        quantity = item['quantity']
      ).save()
      self.assertEqual(Items.objects.get(item_id=item['id'], cart_id=test_cart['id']).valid_purchase, False)
      Items.objects.select_related().filter(item_id=item['id'], cart_id=test_cart['id']).update(valid_purchase=True)
      self.assertEqual(Items.objects.get(item_id=item['id'], cart_id=test_cart['id']).valid_purchase, True)
    print('Updated Purchase from False to True')


###Services API ACTIONS

class Cart_Services_Test(TestCase):

  def setUp(self):

    self.cart = {
      'id': 54000,
      'user_id': 23,
      'shipping_cost': 7.60,
      'subtotal': 148.00,
      'item_list': [{
            'id': 780,
            'shipping_cost': 9.86,
            'item_price': 100.00,
            'valid_purchase': False,
            'quantity': 3
            },
            {
            'id': 560,
            'shipping_cost': 5.00,
            'item_price': 40.00,
            'valid_purchase': False,
            'quantity': 2
            }]
    }


  def test_cart_checkout(self):
    """
      Cart will save when sent cart information
    """

    test_cart = self.cart
    message = cart_checkout(test_cart, print)
    self.assertEqual(len(Items.objects.filter(cart_id=54000)), 2)
    self.assertEqual('Checkout for user 23', message)
    print('Cart Checkout Service Saves Correctly')

  def test_cart_checkout_sends_call(self):
    """
      Cart will send a call to validate order (issue callback)
    """

    test_cart = self.cart
    test_function = MagicMock(return_value=100)
    message = cart_checkout(test_cart, test_function)
    test_function.assert_called_with(test_cart)
    test_function.assert_called_once_with(test_cart)
    print('Cart Checkout Sends Validate Order Call')

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
      "user_id": 46, 
      "id": 2, 
      "shipping_cost": 16.91, 
      "item_list": [
        {
        "item_price": 301.87, 
        "id": 9, 
        "quantity": 5, 
        "shipping_cost": 7.33, 
        "valid_purchase": "False"
        }, 
        {
          "item_price": 251.55, 
          "id": 7, 
          "quantity": 5, 
          "shipping_cost": 9.58, 
          "valid_purchase": "False"}
        ], 
        "subtotal": 2767.1}

    self.test_data2 = {
      "user_id": 55, 
      "id": 9, 
      "shipping_cost": 17.86, 
      "item_list": [{
        "item_price": 184.92, 
        "id": 20, 
        "quantity": 3, 
        "shipping_cost": 9.63, 
        "valid_purchase": "False"
        }, 
        {
        "item_price": 338.17, 
        "id": 14, 
        "quantity": 4, 
        "shipping_cost": 8.23, 
        "valid_purchase": "False"
        }], 
      "subtotal": 1907.44}

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

    url = "http://localhost:8000/purchases/"
    response = self.client.post(url, self.test_data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(response.body.message, 'Order Already Placed')

  def test_create_cart_insertion(self):
    """
      Should check that the model is created from the API endpoint
    """

    url = "http://localhost:8000/purchases/"
    response = self.client.post(url, self.test_data, format='json')
    self.assertEqual(response.status_code, 201)
    self.assertEqual(Carts.objects.count(), 1)
    self.client.post(url, self.test_data2, format='json')
    self.assertEqual(Carts.objects.count(), 2)
    print('Cart Insertion Correctly')

  def request_stock_verification(self):
    """
      Should send a get request to external inventory when receives cart information
    """
    url = "http://localhost:8000/purchases/"
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





