from django.urls import path
from . import views

urlpatterns =[
    path('',views.CART,name='cart'),
    path('add_cart/<int:product_id>/', views.add_cart, name='add_to_cart'),
    path('Minus_cart/<int:product_id>/<int:cart_item_id>/', views.RemoveCart, name='Remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.Cart_ItemRemove, name='Remove_cart_item'),
    # checkout
    path('checkout/',views.Checkout,name='checkout')
    
]
