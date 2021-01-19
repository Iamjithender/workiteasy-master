from django.db import models
# Create your models here.
from django.contrib.auth.models import AbstractUser
from datetime import datetime,date
from django.urls import reverse_lazy,reverse
# import weekday_field
from django.utils import timezone 
from multiselectfield import MultiSelectField

class User(AbstractUser):
    is_customer =models.BooleanField(default=False)
    is_mediator =models.BooleanField(default=False)
    phonenumber =models.PositiveIntegerField(default=9059762161,null=True,blank=True)
    def __str__(self):
        return self.username

class CustomerInfo(models.Model):
    user        =models.OneToOneField(User,on_delete=models.CASCADE)
    location    =models.CharField(max_length=256,blank=True,default="India")
    profile_pic =models.ImageField(upload_to='customer_profile_pics',blank=True)

    def __str__(self):
        return self.user.username


class MediatorInfo(models.Model):
    department_choices=[
        ('',''),
        ('Regional Transport Office','Regional Transport Office'),
        ('Mandal Revenue Office','Mandal Revenue Office'),
        ('Mandal Development Office','Mandal Development Office'),
        ('Roads and Buildings Department','Roads and Buildings Department'),
        ('BANKS','Banks'),
        ('Registration Office','Registration Office'),
    ]
        
    weekday_choices=[
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
        ('Saturday','Saturday'),
        ('Sunday','Sunday'),
    ]
    
    user            =models.OneToOneField(User,on_delete=models.CASCADE)
    location        =models.CharField(max_length=256,blank=True,default="India")
    department      =models.CharField(max_length=256,blank=True,default="RTO",choices=department_choices)
    profile_pic     =models.ImageField(upload_to='mediator_profile_pics',blank=True)
    number_of_ratings=  models.IntegerField(default=0)
    avg_rating      =models.FloatField(default=0)
    weekdays        = MultiSelectField(choices=weekday_choices ,blank=True )  
    unavailable_days=MultiSelectField(blank=True)
    
    def __str__(self):
        return self.user.username


class Connect(models.Model):
    customer            =models.ForeignKey(CustomerInfo,on_delete=models.CASCADE,related_name='connectcustomer')
    mediator            =models.ForeignKey(MediatorInfo,on_delete=models.CASCADE,related_name='connectmediator')
    status              =models.IntegerField(default=0)
    start_date          =models.DateTimeField(default=timezone.now)
    assured_date        =models.DateTimeField(blank=True,null=True)
    completed_date      =models.DateTimeField(blank=True,null=True)
    request_description =models.CharField(max_length=256, blank=True,null=True)
    reject_description  =models.CharField(max_length=256,blank=True,null=True)
    accepted_description=models.CharField(max_length=256,blank=True,null=True)
    customer_seen       =models.BooleanField(default=False)
    mediator_seen       =models.BooleanField(default=False)

    def __str__(self):
        return ("{} is connected to {} with {}".format(self.customer.user.username,self.mediator.user.username,self.status))

class Reviews(models.Model):
    customer    =models.ForeignKey(CustomerInfo,on_delete=models.CASCADE)
    mediator    =models.ForeignKey(MediatorInfo,on_delete=models.CASCADE)
    comment     =models.TextField(max_length=512,blank=True,null=True)
    rating_choices=[
        (1,'very poor'),
        (2,'poor'),
        (3,'average'),
        (4,'good'),
        (5,'excellent'),
    ]
    rating      =models.SmallIntegerField(choices=rating_choices,default=0)
    review_date =models.DateTimeField(default=timezone.now)
    likes       =models.IntegerField(default=0)
    def __str__(self):
        return ("{} is commented on {}".format(self.customer.user.username,self.mediator.user.username))
    

class NotAvailableDates(models.Model):
    mediator    =models.ForeignKey(MediatorInfo,on_delete=models.CASCADE,related_name='non_available_dates')
    date        =models.DateField(blank=True,null=True)
    
    def __str__(self):
        return self.mediator.user.username

class Chats(models.Model):
    customer=models.ForeignKey(CustomerInfo,on_delete=models.CASCADE,related_name='customerswhochatted')
    mediator=models.ForeignKey(MediatorInfo,on_delete=models.CASCADE,related_name='mediatorswhochatted')


class Messages(models.Model):
    chats=models.ForeignKey(Chats,on_delete=models.CASCADE,related_name="chatmessages")
    message=models.CharField(max_length=560)
    is_seen=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=False)
    date=models.DateTimeField(default=timezone.now)





# time        =models.TimeField(default=datetime.now())#default='20:00'