from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponse,HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from shop.models import Product,Variation
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
def add_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)
    product_variation = []

    # Handle variations if method is POST
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                continue

    # Determine cart for authenticated users
    if current_user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=current_user)
        cart_item_query = CartItem.objects.filter(product=product, cart=cart)
    else:
        cart_id = _cart_id(request)
        cart, created = Cart.objects.get_or_create(cart_id=cart_id)
        cart_item_query = CartItem.objects.filter(product=product, cart=cart)

    # Check if the item already exists in the cart
    if cart_item_query.exists():
        ex_vari_list = []
        item_ids = []

        for item in cart_item_query:
            existing_variation = item.variations.all()
            ex_vari_list.append(list(existing_variation))
            item_ids.append(item.id)

        # Check if the product variation already exists
        if product_variation in ex_vari_list:
            index = ex_vari_list.index(product_variation)
            item_id = item_ids[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1  # Increase quantity by 1
            item.save()
        else:
            # Create a new CartItem for the new variation
            item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user if current_user.is_authenticated else None,
                cart=cart  # Link the cart here
            )
            if product_variation:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:
        # Create a CartItem if it doesn't exist
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            user=current_user if current_user.is_authenticated else None,
            cart=cart  # Link the cart here
        )
        if product_variation:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()

    return redirect('cart')
def RemoveCart(request, product_id, cart_item_id):
    
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return redirect('cart')
        else:
            cart_item.delete()
            return redirect('cart')
    except:
       return redirect('cart') 
def Cart_ItemRemove(request,product_id,cart_item_id):
    
    
    product = get_object_or_404(Product,id=product_id)
    if request.user.is_authenticated:
         cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))     
        cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
        
    
def CART(request,total=0,quantity=0,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total +=  (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = tax + total    
    except ObjectDoesNotExist:
        pass
    return render(request, 'cart.html', {
        'cart_items':cart_items,'total':total,'quantity':quantity,
        'tax':tax,'grand_total':grand_total
        
    })
    
@login_required(login_url='login')    
def Checkout(request,total=0,quantity=0,cart_items=None):
    try:
        grand_total = 0
        tax = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total +=  (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = tax + total    
    except ObjectDoesNotExist:
        pass
    return render(request, 'accounts/checkout.html', {
        'cart_items':cart_items,'total':total,'quantity':quantity,
        'tax':tax,'grand_total':grand_total
        
    })
    