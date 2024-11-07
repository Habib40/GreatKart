from django.shortcuts import render,get_object_or_404
from django.http import Http404
from .models import Product
from category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# Create your views here.
def index(request):
    products = Product.objects.filter(is_available=True)
    return render(request, 'index.html',{'products':products})



def OureStore(request, category_slug=None):
    category = None
    products = None
    count = 0  # Initialize count

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)  # Use correct field name
        paginator = Paginator(products,6) # Show 6 products in per page
        page = request.GET.get('page')
        pagged_products = paginator.get_page(page)
        count = products.count()
    else:
        products = Product.objects.filter(is_available=True).order_by('id')
        paginator = Paginator(products,6) # Show 6 products in per page
        page = request.GET.get('page')
        pagged_products = paginator.get_page(page)
        count = products.count()  # Count the number of available products
        
    return render(request, 'store.html', {
        'products': pagged_products, 'count': count,
    })

def ProductDetails(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    chack_in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()
   
    return render(request, 'product_detail.html',{'product':product,'chack_in_cart':chack_in_cart})

from django.db.models import Q

def Search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_at').filter(
                Q(description__icontains=keyword) | Q(name__icontains=keyword)
            )
            count = products.count()  # Count the number of available products
            return render(request, 'store.html', {'products': products,'count':count})


