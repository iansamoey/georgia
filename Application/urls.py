from django.urls import path
from . import views
from .views import add_to_cart


urlpatterns = [
    path('', views.home, name="App-home"),
    path('about/', views.about, name="App-about"),
    path('services/', views.services, name="App-services"),
    path('contact/', views.contact, name="App-contact"),
    path('pricing/', views.pricing, name="App-pricing"),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:service_id>/',
         views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:order_id>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('update-order/', views.update_order, name='update_order'),
    path('update-pending-order/', views.update_pending_order,
         name='update_pending_order'),
    path('pending-orders/', views.pending_orders_view, name='pending_orders_view'),
]
