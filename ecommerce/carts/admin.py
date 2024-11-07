from django.contrib import admin
from .models import Cart,CartItem
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')
    
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'various', 'is_active')
    def various(self, obj):
        return ', '.join([str(variation) for variation in obj.variations.all()])
    filter_horizontal = ('variations',)  # or filter_vertical = ('variations',)

admin.site.register(CartItem, CartItemAdmin)


admin.site.register(Cart,CartAdmin)
