from django.contrib import admin
from.models import Product,Variation
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name','id','category','stock','created_at','modified_at',)
    def category_name(self, obj):
        return obj.category.name
    
class VariationAdmin(admin.ModelAdmin):
     list_display = ('product','variation_category','variation_value','is_active','created_date',)
     list_editable = ('is_active',)
     list_filter = ('product','variation_category','variation_value','created_date',)
admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)