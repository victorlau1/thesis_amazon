from rest_framework import routers
from server import views
from django.conf.urls import url, include

# router = routers.SimpleRouter()
# router.register(r'purchases', views.cart_detail, base_name='purchases')

urlpatterns = [
  url(r'^purchases/$', views.cart_detail),
  url(r'api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]





