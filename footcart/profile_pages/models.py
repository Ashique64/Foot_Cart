from django.db import models
from home.models import user_details 

# Create your models here.

class Address(models.Model):
    user=models.ForeignKey(user_details,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=50)
    phone_number=models.BigIntegerField()
    pincode=models.BigIntegerField()
    locality=models.CharField(max_length=50)
    address=models.CharField(max_length=150)
    district=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    landmark=models.CharField(max_length=50,blank=True,null=True)
    alter_phone=models.CharField(max_length=15,blank=True,null=True)
   
    
    
    def __str__(self):
        return self.full_name
    
    
class Wallet(models.Model):
    user = models.ForeignKey(user_details,on_delete=models.CASCADE)
    wallet_balance = models.IntegerField()
    
    
