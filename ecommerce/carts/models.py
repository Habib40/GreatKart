from django.db import models
from shop.models import Product,Variation
from account.models import Account
import uuid
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    cart_id = models.CharField(max_length=250,blank=True,default=str(uuid.uuid4()))
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    variations = models.ManyToManyField(Variation,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"Cart item for {self.product.name}"
