from .import views
from django.urls import path

urlpatterns =[
    
    path('place_order',views.PlaceOrder,name='place_order'),
    path('payments/',views.Payments,name='payments')
   
]
