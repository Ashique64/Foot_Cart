from django.db import models
from home.models import user_details
from admin_page.models import Product,My_Order,Variants

# Create your models here.

    
    
class Cart(models.Model):
    user = models.ForeignKey(user_details,on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return self.user.username
    
class Cart_items(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    

class Order_items(models.Model):
    order = models.ForeignKey(My_Order,on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
