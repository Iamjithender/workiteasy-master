from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.
from . import models
from . import forms
from .decorators import customer_only,mediator_only,customerloginonly,mediatorloginonly


from django.views.generic import TemplateView,CreateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse

from django.core.mail import send_mail
from datetime import datetime,date
from django.utils import timezone


@customerloginonly
@login_required(login_url='/home/')
def customerIndexView(request):
    mediators=models.MediatorInfo.objects.all()
    customer=models.CustomerInfo.objects.get(user=request.user)
    if request.method == 'POST':
        form=forms.CustomerSearchForm(request.POST)
        if form.is_valid():
            location=form.cleaned_data['location']
            department=form.cleaned_data['department']
            date=form.cleaned_data['date']
            if location and department:
                mediators=models.MediatorInfo.objects.all().filter(department__exact=department).filter(location__exact=location)
            elif location:
                mediators=models.MediatorInfo.objects.all().filter(location__exact=location)
            elif department:
                mediators=models.MediatorInfo.objects.all().filter(department__exact=department)
            
            
            new=models.MediatorInfo.objects.none()
            temp=mediators
            if date:
                newmediators=temp.exclude(unavailable_days__contains=date)
                mediators=newmediators
            days=request.POST.getlist('list')
            temp=mediators
            new=models.MediatorInfo.objects.none()
            if days:
                for day in days:
                    newmediators=temp.filter(weekdays__contains=day)
                    print(newmediators)
                    new=new.union(newmediators)
                    temp=mediators
                print(new)
                mediators=new
    mediators=mediators.order_by('-avg_rating')
    form=forms.CustomerSearchForm() 
    return render(request,'customer/customer_index.html',{'mediators':mediators,'form':form,'customer':customer,})

@mediatorloginonly
@login_required(login_url='/home/')
def mediatorIndexView(request):
    user=request.user
    mediator=models.MediatorInfo.objects.get(user=user)
    allobj=models.Connect.objects.filter(mediator=mediator).order_by('-start_date')
    return render(request,'mediator/mediator_index.html',{'allobj':allobj,})



def customerSignupView(request):
    if request.method == 'POST':
        form = forms.CustomerSignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=request.POST['username']
            email=request.POST['email'] 
            customer=models.CustomerInfo.objects.get(user=user)
            if 'profile_pic' in request.FILES:
                customer.profile_pic=request.FILES['profile_pic']
            customer.save()
            send_mail(
                'FROM WORKEASY.COM',
                'HELLO {} \n Thanks for signing up in our page! \n visit our app and make your works easy and simple'.format(username),
                'work.easy.2525@gmail.com',
                [email,],
                fail_silently=False,
            )
            form=forms.CustomerSignupForm()
            return redirect('accounts:customerlogin')
    else:
        form=forms.CustomerSignupForm()
    return render(request,'customer/customer_signup.html',{'form':form,})



def customerLoginView(request):
    if request.method == 'POST':
        form=forms.CustomerLoginForm(request.POST)
        if form.is_valid():
            username1=form.cleaned_data.get('username')
            password1=form.cleaned_data.get('password')
            user=authenticate(username=username1,password=password1,is_customer=True)
            if user:
                if user.is_active:
                    login(request,user)
                    form=forms.CustomerLoginForm()
                    return HttpResponseRedirect(reverse('accounts:customerindex'))
                else:
                    return HttpResponse("user is not active")
            else:
                form=forms.CustomerLoginForm()
                return HttpResponse("Invalid login details supplied!")
        else:
            print("Error form, invalid!")
    else:
        form=forms.CustomerLoginForm()
    return render(request,'customer/customer_login.html',{'form':form,})




def mediatorSignupView(request):
    if request.method == 'POST':
        form=forms.MediatorSignupForm(request.POST)
        if form:
            if form.is_valid():
                user=form.save()
                mediator = models.MediatorInfo.objects.create(user=user) 
                mediator.location=form.cleaned_data["location"]
                if 'profile_pic' in request.FILES:
                    mediator.profile_pic=request.FILES['profile_pic']
                mediator.department=form.cleaned_data["department"]
                values=request.POST.getlist('list')
                mediator.weekdays=values 
                mediator.save()
                form=forms.MediatorSignupForm()
                email=user.email
                send_mail(
                    'FROM WORKEASY.COM',
                    'HELLO {} \n Thanks for signing up in our page! \n we will let know the customers of your presence'.format(user.username),
                    'work.easy.2525@gmail.com',
                    [email,],
                    fail_silently=False,
                )
                return redirect(reverse('accounts:mediatorlogin'))
    else:
        form=forms.MediatorSignupForm()
    return render(request,'mediator/mediator_signup.html',{'form':form,})



def mediatorLoginView(request):
    if request.method == 'POST':
        form=forms.CustomerLoginForm(request.POST)
        if form.is_valid():
            username1=form.cleaned_data.get('username')
            password1=form.cleaned_data.get('password')
            user=authenticate(username=username1,password=password1)
            if user:
                if user.is_active:
                    login(request,user)
                    form=forms.CustomerLoginForm()
                    return HttpResponseRedirect(reverse('accounts:mediatorindex'))
                else:
                    return HttpResponse("user is not active")
            else:
                form=forms.CustomerLoginForm()
                return HttpResponse("Invalid login details supplied!")
        else:
            print("Error form, invalid!")
    else:
        form=forms.MediatorLoginForm()
    return render(request,'mediator/mediator_login.html',{'form':form,})

@customer_only
@login_required(login_url='/home/')
def customerLogoutView(request):
    logout(request)
    return redirect('home')

@mediator_only
@login_required(login_url='/home/')
def mediatorLogoutView(request):
    logout(request)
    return redirect('home')



@customer_only
@login_required(login_url='/home/')
def customerMediatorDetailView(request,pk1,pk2):
    mediator=models.MediatorInfo.objects.get(pk=pk2)
    customer=models.CustomerInfo.objects.get(pk=pk1)
    if request.method == 'POST':
        if models.Connect.objects.filter(customer=customer,mediator=mediator,status=1).exists():
            return HttpResponse("already both are connected")
        
        connection=models.Connect.objects.create(mediator=mediator,customer=customer)
        des=request.POST['Description']
        if des:
            connection.request_description=des
            connection.save() 
        connection.status=1
        connection.customer_seen=False
        connection.mediator_seen=False
        time=datetime.now()
        connection.start_date=datetime.now()
        connection.save()
        return redirect( 'accounts:connectcustomermediator',pk1=pk1,pk2=pk2)

    ratings=models.Reviews.objects.filter(mediator=mediator).order_by('-review_date')
    connect=False
    if models.Connect.objects.filter(customer=customer,mediator=mediator,status=(1 or 2)).exists():
        connect=True
    form=forms.DescriptionForm()

    form.fields['Description'].widget.attrs['label']=" "
    return render(request,'customer/customer_mediator_detail.html',{'mediator':mediator,
                                                            'customer':customer,
                                                            'connect':connect,
                                                            'ratings':ratings,
                                                            'form':form,
                                                            'pk1':pk1,
                                                            'pk2':pk2,
                                                            })


@customer_only
@login_required(login_url='/home/')
def connectCustomerMediator(request,**kwargs):
    pk1=kwargs['pk1']
    pk2=kwargs['pk2']
    customer=models.CustomerInfo.objects.get(pk=pk1)
    mediator=models.MediatorInfo.objects.get(pk=pk2)
    connect=models.Connect.objects.filter(customer=customer,mediator=mediator,status=1)
    time=datetime.now()
    return render(request,'customer/connect_customer_mediator.html',{'mediator':mediator,
                                                                     'customer':customer,
                                                                    'time':time,
                                                                    'connect':connect})


@mediator_only
@login_required(login_url='/home/')
def acceptCustomerMediator(request,**kwargs):
    pk1=kwargs['pk1']
    pk2=kwargs['pk2']
    customer=models.CustomerInfo.objects.get(pk=pk1)
    mediator=models.MediatorInfo.objects.get(pk=pk2)
    connection=models.Connect.objects.filter(mediator=mediator,customer=customer,status=1).update(status=2,assured_date=datetime.now(),customer_seen=False,mediator_seen=False)
    email=customer.user.email
    send_mail(
        'FROM WORKEASY.COM',
        'HELLO THERE THE MEDIATOR {} ACCEPTED YOUR REQUEST AT {} NOW YOU CAN FURTHER PROCEED BY CONTACTING HIM'.format(mediator.user.username,datetime.now()),
        'work.easy.2525@gmail.com',
        [email,],
        fail_silently=False,
    )
    return render(request,'mediator/accept_customer_mediator.html',{'mediator':mediator,
                                                                     'customer':customer,
                                                                    'time':datetime.now()})


@mediator_only
@login_required(login_url='/home/')
def mediatorRequestsView(request):
    mediator=models.MediatorInfo.objects.get(user=request.user)
    connects=models.Connect.objects.all().filter(mediator=mediator,status__exact=1)
    return render(request,'mediator/mediator_requests_list_page.html',{'connects':connects,})


@mediator_only
@login_required(login_url='/home/')
def mediatorAcceptedView(request):
    mediator=models.MediatorInfo.objects.get(user=request.user)
    connects=models.Connect.objects.all().filter(mediator=mediator,status__exact=2)
    return render(request,'mediator/mediator_accepted_list_page.html',{'connects':connects,})


@mediator_only
@login_required(login_url='/home/')
def mediatorRejectedView(request):
    mediator=models.MediatorInfo.objects.get(user=request.user)
    connects=models.Connect.objects.all().filter(mediator=mediator,status__exact=3)
    return render(request,'mediator/mediator_rejected_list.html',{'connects':connects,})

@mediator_only
@login_required(login_url='/home/')
def mediatorCompletedView(request):
    mediator=models.MediatorInfo.objects.get(user=request.user)
    connects=models.Connect.objects.all().filter(mediator=mediator,status__exact=4)
    return render(request,'mediator/mediator_completed_list.html',{'connects':connects,})

@mediator_only
@login_required(login_url='/home/')
def mediatorCancelledView(request):
    mediator=models.MediatorInfo.objects.get(user=request.user)
    connects=models.Connect.objects.all().filter(mediator=mediator,status__exact=5)
    return render(request,'mediator/mediator_cancelled_list.html',{'connects':connects,})

@mediator_only
@login_required(login_url='/home/')
def mediatorProfileView(request):
    mediator=models.MediatorInfo.objects.get(user=request.user)
    non_available_dates=models.NotAvailableDates.objects.filter(mediator=mediator,date__gte=date.today()).order_by('date') 
    return render(request,'mediator/mediator_profile.html',{'mediator':mediator,
                                                            'dates':non_available_dates})


@mediator_only
@login_required(login_url='/home/')
def mediatorProfileEditView(request):
    form = forms.MediatorEditForm()
    user=request.user
    mediator=models.MediatorInfo.objects.get(user=user) 
    if request.method == 'POST':
        form=forms.MediatorEditForm(request.POST)
        if form.is_valid:
            username=request.POST['username']
            password=request.POST['password']
            email=request.POST['email'] 
            location=request.POST['location']
            department=request.POST['department']
            phonenumber=request.POST['phonenumber']
            
                # if mediator.unavailable_days:
                #     mediator.unavailable_days=mediator.unavailable_days.append(date)
                #     print(mediator.unavailable_days)
                # else:
                #     mediator.unavailable_days=date
                #     mediator.save() 
                #     print(mediator.unavailable_days)
            users=models.User.objects.all()
            users_usernames=[]
            for user1 in users:
                users_usernames.append(user1.username)
            if username and username not in users_usernames:
                user.username=username
            user.save()
            if password:
                user.set_password(password)
            if email:
                user.email=email
            user.save()
            login(request,user)
            mediator.user=user
            if location:
                mediator.location=location
            if department:
                mediator.department=department 
            if phonenumber:
                mediator.phonenumber=phonenumber
            if 'profile_pic' in request.FILES:
                print("profile_pic is uploaded")
                mediator.profile_pic=request.FILES['profile_pic']
            days=request.POST.getlist('list')
            date=request.POST['date'] 
            if len(days) != 0:
                mediator.weekdays=days
            if len(date) !=0 :
                if date not in mediator.unavailable_days:
                    mediator.unavailable_days.append(date)
                print(mediator.unavailable_days)
            mediator.save()
            print(mediator.unavailable_days)
            return redirect(reverse('accounts:mediatorprofile'))
    form.fields['username'].widget.attrs['placeholder']=mediator.user.username
    form.fields['email'].widget.attrs['placeholder']=mediator.user.email
    form.fields['location'].widget.attrs['placeholder']=mediator.location
    form.fields['department'].widget.attrs['label']="Present Department:{}".format(mediator.department)
    form.fields['phonenumber'].widget.attrs['placeholder']=mediator.user.phonenumber
    form.fields['date'].widget.attrs['label']="Unavailable Dates"
    return render(request,'mediator/mediator_profile_edit.html',{'form':form,'mediator':mediator})


@customer_only
@login_required
def customerNotificationsView(request):
    customer=models.CustomerInfo.objects.get(user=models.User.objects.get(username=request.user.username))
    notifications=models.Connect.objects.filter(customer=customer,customer_seen=False)
    for notification in notifications:
        notification.customer_seen=True
        notification.save()
    chats=models.Messages.objects.filter(is_customer=False,is_seen=False)
    updates=chats
    updates.update(is_seen=True)
    return render(request,'customer/customer_notifications.html',{'connects':notifications,'chats':chats})


@mediator_only
@login_required
def mediatorNotificationsView(request):
    mediator=models.MediatorInfo.objects.get(user=models.User.objects.get(username=request.user.username))
    notifications=models.Connect.objects.filter(mediator=mediator,mediator_seen=False).order_by('completed_date','-start_date')
    for notifi in notifications:
        notifi.mediator_seen=True
        notifi.save()
    chats=models.Messages.objects.filter(is_customer=False,is_seen=False)
    updates=chats
    updates.update(is_seen=True)
    return render(request,'mediator/mediator_notifications.html',{'connects':notifications,'chats':chats})



@customer_only
@login_required(login_url='/home/')
def customerProfileView(request):
    customer=models.CustomerInfo.objects.get(user=request.user)
    return render(request,'customer/customer_profile.html',{'customer':customer,})


@customer_only
@login_required(login_url='/home/')
def customerProfileEditView(request):
    form = forms.CustomerEditForm()
    user=models.User.objects.get(username__exact=request.user.username)
    customer=models.CustomerInfo.objects.get(user=user)
    if request.method == 'POST':
        form=forms.CustomerEditForm(request.POST)
        if form.is_valid:
            username=request.POST['username']
            password=request.POST['password']
            email=request.POST['email'] 
            location=request.POST['location']
            phonenumber=request.POST['phonenumber']
            users=models.User.objects.all()
            users_usernames=[]
            for user1 in users:
                users_usernames.append(user1.username)
            if username and username not in users_usernames:
                user.username=username
            user.save()
            if password:
                user.set_password(password)
            user.save()
            login(request,user)
            customer.user=user
            if location:
                customer.location=location
            if phonenumber:
                customer.phonenumber=phonenumber
            if 'profile_pic' in request.FILES:
                customer.profile_pic=request.FILES['profile_pic']
            customer.save()
            return redirect('accounts:customerprofile')
    form.fields['username'].widget.attrs['placeholder']=customer.user.username
    form.fields['email'].widget.attrs['placeholder']=customer.user.email
    form.fields['location'].widget.attrs['placeholder']=customer.location
    form.fields['phonenumber'].widget.attrs['placeholder']=customer.user.phonenumber
    return render(request,'customer/customer_profile_edit.html',{'form':form,})


@customer_only
@login_required(login_url='/home/')
def customerRequestsView(request):
    customer=models.CustomerInfo.objects.get(user=request.user)
    connects=models.Connect.objects.all().filter(customer=customer,status__exact=1).order_by('start_date')
    return render(request,'customer/customer_requests_list_page.html',{'connects':connects,})


@customer_only
@login_required(login_url='/home/')
def customerAcceptedView(request):
    customer=models.CustomerInfo.objects.get(user=request.user)
    connects=models.Connect.objects.all().filter(customer=customer,status__exact=2)
    return render(request,'customer/customer_accepted_list_page.html',{'connects':connects,})

@customer_only
@login_required(login_url='/home/')
def customerRejectedView(request):
    customer=models.CustomerInfo.objects.get(user=request.user)
    connects=models.Connect.objects.all().filter(customer=customer,status__exact=3)
    return render(request,'customer/customer_rejected.html',{'connects':connects,})

@customer_only
@login_required(login_url='/home/')
def customerCompletedView(request):
    customer=models.CustomerInfo.objects.get(user=request.user)
    connects=models.Connect.objects.all().filter(customer=customer,status__exact=4)
    return render(request,'customer/customer_completed.html',{'connects':connects,})

@customer_only
@login_required(login_url='/home/')
def customerCancelledView(request):
    customer=models.CustomerInfo.objects.get(user=request.user)
    connects=models.Connect.objects.all().filter(customer=customer,status__exact=5)
    return render(request,'customer/customer_cancelled.html',{'connects':connects,})

@customer_only
@login_required(login_url='/home/')
def cancelConnectionView(request,pk):
    connects=models.Connect.objects.get(pk=pk)
    if not connects:
        return redirect('accounts:customersaccepted')   
    connects.completed_date=datetime.now()
    connects.customer_seen=False
    connects.status=5
    connects.save()
    return redirect('accounts:customersaccepted')

@customer_only
@login_required(login_url='/home/')
def customerHistoryView(request):
    customer=models.CustomerInfo.objects.get(user=request.user)
    connects=models.Connect.objects.filter(customer=customer).order_by('-completed_date','assured_date','start_date')
    return render(request,'customer/customer_history.html',{'connects':connects,})


@customer_only
@login_required(login_url='/home/')
def rateMediatorView(request,pk1,pk2):
    form=forms.RateMediatorForm()
    if request.method == 'POST':
        rating=request.POST['rating']
        comment=request.POST['comment']
        customer=models.CustomerInfo.objects.get(pk=pk1)
        mediator=models.MediatorInfo.objects.get(pk=pk2)
        prev_rating=mediator.avg_rating
        count=mediator.number_of_ratings
        print("{} this is the rating provided".format(rating))
        temp=count*prev_rating+float(rating)

        if models.Reviews.objects.filter(customer=customer,mediator=mediator).exists():
            prev=get_object_or_404(models.Reviews,customer=customer,mediator=mediator)
            temp=temp-prev.rating
            avg=temp/count
        else:
            avg=(temp)/(count+1)
            count=count+1
        mediator.avg_rating=avg
        mediator.number_of_ratings=count
        mediator.save()
        rateobject=models.Reviews.objects.get_or_create(customer=customer,mediator=mediator)[0]
        rateobject.review_date=datetime.now()
        rateobject.rating=rating
        if comment:
            rateobject.comment=comment
        rateobject.save()
        return redirect('accounts:customermediatordetail',pk1=pk1,pk2=pk2)
    return render(request,'customer/customer_rate_mediator.html',{'form':form,'pk1':pk1,'pk2':pk2,})

@mediator_only
@login_required(login_url='/home/')
def mediatorHistoryView(request):
    mediator=models.MediatorInfo.objects.get(user=request.user)
    connects=models.Connect.objects.filter(mediator=mediator).order_by('completed_date','assured_date','-start_date')
    return render(request,'mediator/mediator_history.html',{'connects':connects,})

@mediator_only
@login_required(login_url='/home/')
def rejectCustomerView(request,**kwargs):
    pk1=kwargs['pk1']
    pk2=kwargs['pk2']
    customer=models.CustomerInfo.objects.get(pk=pk1)
    mediator=models.MediatorInfo.objects.get(pk=pk2)
    connection=models.Connect.objects.filter(mediator=mediator,customer=customer,status=1).update(completed_date=datetime.now(),status=3,customer_seen=False,mediator_seen=False)
    return redirect('accounts:mediatorindex')

@mediator_only
@login_required(login_url='/home/')
def completeConnectionView(request,**kwargs):
    pk1=kwargs['pk1']
    pk2=kwargs['pk2']
    customer=models.CustomerInfo.objects.get(pk=pk1)
    mediator=models.MediatorInfo.objects.get(pk=pk2)
    connection=models.Connect.objects.filter(mediator=mediator,customer=customer,status=2).update(completed_date=datetime.now(),status=4,customer_seen=False,mediator_seen=False)
    return redirect('accounts:mediatorindex')

@mediator_only
@login_required(login_url='/home/')
def mediatorReviewsView(request):
    mediator=models.MediatorInfo.objects.get(user=models.User.objects.get(username=request.user.username))
    ratings=models.Reviews.objects.filter(mediator=mediator).order_by('-review_date')
    print(ratings)
    return render(request,'mediator/mediator_reviews.html',{'ratings':ratings})
 



@customer_only
@login_required(login_url='/home/')
def customerChatsView(request,pk1,pk2):
    customer=models.CustomerInfo.objects.get(pk=pk1)
    mediator=models.MediatorInfo.objects.get(pk=pk2)
    chats=models.Chats.objects.get_or_create(customer=customer,mediator=mediator)[0]
    form=forms.MessageForm()
    if request.method == 'POST':
        customerchats=models.Messages.objects.create(chats=chats)
        customerchats.message=request.POST['message']
        customerchats.is_customer=True
        customerchats.date=timezone.now()
        customerchats.save()  
        return redirect('accounts:customerchats',pk1=pk1,pk2=pk2)
    temp=models.Messages.objects.filter(chats=chats)
    return render(request,'customer/customer_chats.html',{
                                                        'messages':temp,'form':form,})

    
@mediator_only
@login_required(login_url='/home/')
def mediatorChatsView(request,pk1,pk2):
    customer=models.CustomerInfo.objects.get(pk=pk1)
    mediator=models.MediatorInfo.objects.get(pk=pk2)
    chats=models.Chats.objects.get_or_create(customer=customer,mediator=mediator)[0]
    form=forms.MessageForm()
    if request.method == 'POST':
        mediatorchats=models.Messages.objects.create(chats=chats)
        mediatorchats.message=request.POST['message']
        mediatorchats.date=timezone.now()
        mediatorchats.save()  
        return redirect('accounts:mediatorchats',pk1=pk1,pk2=pk2)
    temp=models.Messages.objects.filter(chats=chats)
    return render(request,'mediator/mediator_chats.html',{'form':form,
                                                        'messages':temp,})

