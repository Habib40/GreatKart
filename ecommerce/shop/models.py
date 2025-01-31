from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.
class Product(models.Model):
    name        =models.CharField(max_length=100)
    slug        =models.SlugField(max_length=50,unique=True)
    description = models.TextField(max_length=500,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.ImageField(upload_to='photos/products')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    stock = models.IntegerField()
    is_available = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    def get_url(self):
      return reverse('product_details', args=[self.category.slug, self.slug])
  
class VariationManager(models.Manager):
     def colors(self):
         return super(VariationManager,self).filter(variation_category='color',is_active=True)
     def sizes(self):
         return super(VariationManager,self).filter(variation_category='size',is_active=True)
  
VARIATION_CATEGORY_CHOICES=(
    ('color','color'),
    ('size','size'),
)    

class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=VARIATION_CATEGORY_CHOICES)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    
    objects = VariationManager()
    def __str__(self):
        return f"{self.variation_category} - {self.variation_value}"