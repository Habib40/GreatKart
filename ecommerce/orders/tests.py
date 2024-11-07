from django.test import TestCase

# Create your tests here.
# def PlaceOrder(request, total=0, tax=0, quantity=0):
#     current_user = request.user
#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()

#     if cart_count <= 0:
#         return redirect('store')

#     grand_total = 0
#     tax = 0
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += cart_item.quantity
    
#     tax = (2 * total) / 100
#     grand_total = total + tax
    
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # Create an order instance
#             order = Order()
#             order.user = current_user
#             order.first_name = form.cleaned_data['first_name']
#             order.last_name = form.cleaned_data['last_name']
#             order.email = form.cleaned_data['email']
#             order.phone = form.cleaned_data['phone']
#             order.address_line_1 = form.cleaned_data['address_line_1']
#             order.address_line_2 = form.cleaned_data['address_line_2']
#             order.country = form.cleaned_data['country']
#             order.state = form.cleaned_data['state']
#             order.city = form.cleaned_data['city']
#             order.order_note = form.cleaned_data['order_note']
#             order.tax = tax
#             order.ip = request.META.get('REMOTE_ADDR')
#             order.order_total = grand_total
#             order.save()

#             # Generate order number
#             yr = int(datetime.date.today().strftime('%y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr, mt, dt)
#             current_date = d.strftime("%Y,%d,%m")
#             order_number = current_date + str(order.id)
#             order.order_number = order_number
#             order.save()

#             # Create OrderProduct instances
#             for cart_item in cart_items:
#                 OrderProduct.objects.create(
#                     order=order,
#                     user=current_user,
#                     product=cart_item.product,
#                     variation=cart_item.variation,  # Make sure to handle variations if needed
#                     quantity=cart_item.quantity,
#                     product_price=cart_item.product.price,
#                     ordered=True
#                 )

#             # Delete cart items after placing the order
#             cart_items.delete()

#             messages.success(request, 'Your order has been placed successfully!')
#             context = {
#                 'order': order,
#                 'cart_items': cart_items,
#                 'total': total,
#                 'tax': tax,
#                 'grand_total': grand_total
#             }
#             return render(request, 'orders/payments.html', context)  # Redirect to payment or confirmation page
#         else:
#             messages.error(request, 'Please correct the errors in the form.')
#             return redirect('checkout')  # Redirect back to checkout page to show the form with errors

#     return render(request, 'checkout.html')  # Render your checkout page if not POST