from django.conf import settings
from django.conf.urls.static import static
from django .urls import path
from .views import (products,add_to_cart,increase_quantity,decrease_quantity,cart,
                    remove_from_cart,cart,checkout,order_success,order_detail,my_orders)

urlpatterns = [
    path('products/',products,name='products'),
    path('add_to_cart/<int:id>',add_to_cart,name='add_to_cart'),
    path('increase_quantity/<int:id>',increase_quantity,name='increase_quantity'),
    path('cart/',cart,name='cart'),
    path('order_success/<int:id>',order_success,name='order_success'),
    path('my_orders/',my_orders,name='my_orders'),
    path('order_detail/<int:id>',order_detail,name='order_detail')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

