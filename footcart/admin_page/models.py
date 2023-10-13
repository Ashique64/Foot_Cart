from django.db import models
from home.models import user_details
from profile_pages.models import Address
from django.utils import timezone
# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Color(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Size(models.Model):
    name=models.PositiveIntegerField()
    
    def __str__(self):
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Variants(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    size = models.ForeignKey(Size,on_delete=models.CASCADE)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discription = models.CharField(max_length=500)
    quantity = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    
    def discounted_price(self):
        if self.discount is not None:
            discounted_amount = (self.price * self.discount) / 100
            return self.price - discounted_amount
        return self.price
    


class My_Order(models.Model):
    user = models.ForeignKey(user_details,on_delete=models.CASCADE)
    address = models.ForeignKey(Address,on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20)
    total_price = models.IntegerField()
    order_date = models.DateField(auto_now_add=True)
    ORDER_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    coupon_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        ordering = ['-order_date']
 
 
       
        
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    discount_type = models.CharField(max_length=20, choices=[
        ('percentage', 'Percentage'),
        ('fixed_amount', 'Fixed Amount'),
    ], default='fixed_amount')
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
class Wishlist(models.Model):
    user = models.ForeignKey(user_details, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"Wishlist - {self.user.username}"