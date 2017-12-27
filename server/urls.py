from rest_framework import routers
from .views import CartViewSet, InventoryViewSet
from django.conf.urls import url, include

router = routers.SimpleRouter()
router.register(r'purchases', CartViewSet, base_name = 'Carts')
router.register(r'validation', InventoryViewSet, base_name = 'Items')

urlpatterns = [
  url(r'^', include(router.urls)),
  url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]





