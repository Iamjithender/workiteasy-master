from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm



class DateInput(forms.DateInput):
    input_type ='date'

class CustomerSignupForm(UserCreationForm):
    location=forms.CharField(max_length=256,required=True)
    profile_pic=forms.ImageField(required=False)
    class Meta:
            model=models.User
            fields=("username","email","password1","password2","phonenumber","location","profile_pic")
        
    def save(self,commit=True):
        user=super().save(commit=False)
        user.is_customer=True
        user.phonenumber=self.cleaned_data["phonenumber"]
        user.set_password(self.cleaned_data["password1"])
        user.save()
        customer = models.CustomerInfo.objects.create(user=user)
        if self.cleaned_data["location"]:
            customer.location=self.cleaned_data["location"]
        customer.save()
        return user


class DescriptionForm(forms.Form):
    Description=forms.CharField(max_length=256,required=False)

 

class MediatorSignupForm(UserCreationForm):
    department_choices=[
        ('RTO','Regional Transport Office'),
        ('MRO','Mandal Revenue Office'),
        ('MDO','Mandal Development Office'),
        ('RBD','Roads and Buildings Department'),
        ('BANKS','Banks'),
        ('REGISTRATION','Registration Office'),
    ]
    location=forms.CharField(max_length=256,required=True)
    department=forms.CharField(max_length=256,required=True,widget=forms.Select(choices=department_choices))
    profile_pic=forms.ImageField(required=False)

    class Meta:
        model=models.User
        fields=("username","email","password1","password2","phonenumber","location","department","profile_pic")
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.is_mediator=True
        user.phonenumber=self.cleaned_data["phonenumber"]
        user.set_password(self.cleaned_data["password1"])
        user.save()
        return user







class CustomerLoginForm(forms.Form):
    username=forms.CharField(max_length=256,required=True)
    password=forms.CharField(widget=forms.PasswordInput(),required=True)





class MediatorLoginForm(forms.Form):
    username=forms.CharField(max_length=256,required=True)
    password=forms.CharField(widget=forms.PasswordInput(),required=True)
    


class CustomerSearchForm(forms.Form):
    department_choices=[
        ('',''),
        ('Regional Transport Office','Regional Transport Office'),
        ('Mandal Revenue Office','Mandal Revenue Office'),
        ('Mandal Development Office','Mandal Development Office'),
        ('Roads and Buildings Department','Roads and Buildings Department'),
        ('BANKS','Banks'),
        ('Registration Office','Registration Office'),
        ] 
    location=forms.CharField(max_length=256,required=False)
    department=forms.CharField(max_length=256,required=False, widget=forms.Select(choices=department_choices)) 
    date=forms.DateField(required=False,widget=DateInput) 

class MediatorSearchForm(forms.Form):
    department_choices=[
        ('',''),
        ('Regional Transport Office','Regional Transport Office'),
        ('Mandal Revenue Office','Mandal Revenue Office'),
        ('Mandal Development Office','Mandal Development Office'),
        ('Roads and Buildings Department','Roads and Buildings Department'),
        ('BANKS','Banks'),
        ('Registration Office','Registration Office'),
        ] 
    location=forms.CharField(max_length=256,required=False)
    department=forms.CharField(max_length=256,required=False, widget=forms.Select(choices=department_choices)) 


class MediatorEditForm(forms.Form):
    department_choices=[
        ('',''),
        ('Regional Transport Office','Regional Transport Office'),
        ('Mandal Revenue Office','Mandal Revenue Office'),
        ('Mandal Development Office','Mandal Development Office'),
        ('Roads and Buildings Department','Roads and Buildings Department'),
        ('BANKS','Banks'),
        ('Registration Office','Registration Office'),
        ] 
    username=forms.CharField(max_length=256,required=False)
    password=forms.CharField(widget=forms.PasswordInput(),required=False)
    email=forms.EmailField(max_length=100,required=False)
    location=forms.CharField(max_length=256,required=False)
    department=forms.CharField(max_length=256,required=False, widget=forms.Select(choices=department_choices))
    phonenumber=forms.IntegerField(required=False)
    date=forms.DateField(required=False,widget=DateInput,label="Unavailable Dates")
    profile_pic=forms.ImageField(required=False)


class CustomerEditForm(forms.Form):
    username=forms.CharField(max_length=256,required=False)
    password=forms.CharField(widget=forms.PasswordInput(),required=False)
    email=forms.EmailField(max_length=100,required=False)
    location=forms.CharField(max_length=256,required=False)
    phonenumber=forms.IntegerField(required=False)
    profile_pic=forms.ImageField(required=False)


class RateMediatorForm(forms.Form):
    rating_choices=[
        (1,'very bad'),
        (2,'bad'),
        (3,'average'),
        (4,'good'),
        (5,'excellent'),
    ]
    rating      =forms.IntegerField(widget=forms.Select(choices=rating_choices))
    comment     =forms.CharField(required=False,max_length=100)

class MessageForm(forms.Form): 
    message=forms.CharField(max_length=512,required=True) 

