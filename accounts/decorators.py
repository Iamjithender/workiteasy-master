from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.shortcuts import redirect

def customer_only(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_customer == True:
            return view_func(request,*args,**kwargs)
        else:
            raise Http404("this page is only accessable to customer")
    return wrapper

def customerloginonly(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_customer == True:
            return view_func(request,*args,**kwargs)
        else:
            return redirect('accounts:customerlogin')
    return wrapper

def mediatorloginonly(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_mediator == True:
            return view_func(request,*args,**kwargs)
        else:
            return redirect('accounts:mediatorlogin')
    return wrapper

def mediator_only(view_func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_mediator == True:
            return view_func(request,*args,**kwargs)
        else:
            raise Http404("this page is only accessable to mediator")
    return wrapper

