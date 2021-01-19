from django.shortcuts import render,redirect

# Create your views here.
from . import models
from . import forms
from django.views.generic import TemplateView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse

class IndexView(TemplateView,LoginRequiredMixin):
    template_name='customer/index.html'




def customerSignupView(request):
    if request.method == 'POST':
        form = forms.CustomerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer:customerlogin')
    else:
        form=forms.CustomerSignupForm()
    return render(request,'customer/customersignup.html',{'form':form,})



def customerLoginView(request):
    if request.method == 'POST':
        form=forms.CustomerLoginForm(request.POST)
        if form:
            if form.is_valid():
                username1=form.cleaned_data.get('username')
                password1=form.cleaned_data.get('password')
                user=authenticate(username=username1,password=password1)
                login(request,user)
                return redirect('customer:customerindex')
    else:
        form=forms.LoginForm()
    return render(request,'customer/customerlogin.html',{'form':form,})




def mediatorSignupView(request):
    if request.method == 'POST':
        form=forms.




@login_required
def customerLogoutView(request):
    logout(request)
    return redirect('home')


@login_required
def mediatorLogoutView(request):
    logout(request)
    return redirect('home')





























# class CustomerSignupView(CreateView):
#     model=models.User
#     form_class=forms.CustomerDetailForm
#     template_name='customer/customersignup.html'
#     success_url=reverse_lazy('customer:login')

#     def get_context_data(self,**kwargs):
#         context=super().get_context_data(**kwargs)
#         context['user_type']="customer"
#         return context
    
#     def form_valid(self,form):
#         user = form.save()
#         return HttpResponseRedirect('customer/login/')


            
# class CustomerLoginView(CreateView):
    # model=models.User
    # form_class=forms.LoginForm
    # template_name='customer/customerlogin.html'
    
    # def form_valid(self,form):
    #     username1 =self.cleaned_data["username"]
    #     password1 =self.cleaned_data["password"]
    #     user=authenticate(username=username1,password=password1)
    #     if user:
    #         if user.is_active:
    #             login(self.request,user)
    #             return HttpResponseRedirect(reverse('customer/index'))
    #         else:
    #             return HttpResponse("Account not active")
    #     else:
    #         print("hi")

    

        

    
    