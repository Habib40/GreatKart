from .import views
from django.urls import path

urlpatterns =[
    
    path('',views.OureStore,name='store'),
    path('category/<slug:category_slug>/', views.OureStore, name='store_by_category'),  # For category-specific products
    path('category/<slug:category_slug>/<slug:product_slug>/', views.ProductDetails, name='product_details'),  # For category-specific products
    path('search/',views.Search,name='search')
    
]
