from django.shortcuts import render,redirect
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order,OrderProduct,Payment
import datetime 
from django.contrib import messages
import json
# Create your views here.
def PlaceOrder(request, total=0, tax=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    tax = (2 * total) / 100
    grand_total = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create an order instance
            order = Order()
            order.user = current_user
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.email = form.cleaned_data['email']
            order.phone = form.cleaned_data['phone']
            order.address_line_1 = form.cleaned_data['address_line_1']
            order.address_line_2 = form.cleaned_data['address_line_2']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.order_note = form.cleaned_data['order_note']
            order.tax = tax
            order.ip = request.META.get('REMOTE_ADDR')
            order.order_total = grand_total
            order.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y,%d,%m")
            order_number = current_date + str(order.id)
            order.order_number = order_number
            order.save()

            # Create OrderProduct instances
            for cart_item in cart_items:
                variation = None  # Default to None if no variations are present
                if cart_item.variations.exists():
                    variation = cart_item.variations.first()  # Get the first variation if it exists

                # Create OrderProduct regardless of variation
                order_product = OrderProduct.objects.create(
                    order=order,
                    user=current_user,
                    product=cart_item.product,
                    variation=variation,  # Can be None if no variation exists
                    quantity=cart_item.quantity,
                    product_price=cart_item.product.price,
                    ordered=True
                )

                print(f"Created OrderProduct: {order_product} for product: {cart_item.product.name}")

            # Delete cart items after placing the order
            cart_items.delete()

            messages.success(request, 'Your order has been placed successfully!')
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total
            }
            return render(request, 'orders/payments.html', context)  # Redirect to payment or confirmation page
        else:
            messages.error(request, 'Please correct the errors in the form.')
            return redirect('checkout')  # Redirect back to checkout page to show the form with errors

    return render(request, 'checkout.html')  # Render your checkout page if not POST
        


def Payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['order ID'])
    # Store transaction details inside Payment: model
    payment = Payment(
        user = request.user,
        payment_id = body['transID'],
        payment_method = body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()
    cart_items = CartItem.objects.filter(user=request.user)
    # Move the cart items to Order Product table
    for item in cart_items:
        orderproduct = OrderProduct()
        orderproduct.order_id = order.id
        orderproduct.payment = payment
        orderproduct.user_id = request.user.id
        orderproduct.product_id = item.product_id
        orderproduct.quantity = item.quantity
        orderproduct.product_price = item.product.price
        orderproduct.ordered = True
        orderproduct.save()
    
        cart_item = CartItem.objects.get(id=item.id)
        product_variation = cart_item.variations.all()
        orderproduct = OrderProduct.objects.get(id=orderproduct.id)
        orderproduct.variations.set(product_variation)
        orderproduct.save()
        # Reduce the quantity of the sold products
    cart_items = CartItem.objects.filter(user=request.user).delete()
        # Clear cart
        #Send order recieved email to customer
        # Send order number and transaction id back to sendData method via JsonResponse
            # Delete CartItem after creating order
        
        
        # Redirect to a success page or order confirmation page
     # Change this to your actual confirmation URL
    
    return render(request, 'orders/payments.html')

            
        
    
    