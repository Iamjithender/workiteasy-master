from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_customer =models.BooleanField(default=False)
    is_mediator =models.BooleanField(default=False)
    phonenumber =models.PositiveIntegerField(null=True,blank=True)
    def __str__(self):
        return self.username

class CustomerInfo(models.Model):
    user        =models.OneToOneField(User,on_delete=models.CASCADE)
    location    =models.CharField(max_length=256,blank=True,default="India")

    def get_abs_url(self):
        return reverse("customer:index")
    
    def __str__(self):
        return self.user.username


class MediatorInfo(models.Model):
    user        =models.OneToOneField(User,on_delete=models.CASCADE)
    location    =models.CharField(max_length=256,blank=True,default="India")
    
    def __str__(self):
        return self.user.username


class Connect(models.Model):
    customer    =models.ForeignKey(CustomerInfo,on_delete=models.CASCADE)
    mediator    =models.ForeignKey(MediatorInfo,on_delete=models.CASCADE)
    status      =models.CharField(default="NULL",max_length=256)



# def save(self,*args,**kwargs):
#     super.save(*args,**kwargs)

