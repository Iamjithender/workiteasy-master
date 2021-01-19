from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm




class CustomerSignupForm(UserCreationForm):
    location=forms.CharField(max_length=256,required=True)
    class Meta:
        model=models.User
        fields=("username","email","password1","password2","phonenumber",)
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.is_customer=True
        user.phonenumber=self.cleaned_data["phonenumber"]
        user.password=set_password(self.password1)
        user.save()
        cus = models.CustomerInfo.objects.create(user=user)
        if self.cleaned_data["location"]:
            cus.location=self.cleaned_data["location"]
        cus.save()
        return user






class MediatorSignupForm(UserCreationForm):
    location=forms.CharField(max_length=256,required=True)
    class Meta:
        model=models.User
        fields=("username","email","password1","password2","phonenumber",)
    
    def save(self,commit=True):
        user=super().save(commit=False)
        user.is_mediator=True
        user.phonenumber=self.cleaned_data["phonenumber"]
        user.password=set_password(self.password1)
        user.save()
        cus = models.CustomerInfo.objects.create(user=user)
        if self.cleaned_data["location"]:
            cus.location=self.cleaned_data["location"]
        cus.save()
        return user







class CustomerLoginForm(forms.Form):
    username=forms.CharField(max_length=256,required=True)
    password=forms.CharField(widget=forms.PasswordInput(),required=True)





class MediatorLoginForm(froms.Form):
    username=forms.CharField(max_length=256,required=True)
    password=forms.CharField(widget=forms.PasswordInput(),required=True)
    