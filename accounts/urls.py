from django.conf.urls import url
from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views


app_name='accounts'

urlpatterns=[
    url(r'^customer/$',views.customerIndexView,name='customerindex'),
    url(r'^customerlogin/$', views.customerLoginView,name='customerlogin'),
    url(r'^customerlogout/$', views.customerLogoutView,name='customerlogout'),
    url(r'^customersignup/$',views.customerSignupView,name='customersignup'),
    path('customer/customersrequests/',views.customerRequestsView,name='customersrequests'),
    path('customer/customersaccepted/',views.customerAcceptedView,name='customersaccepted'),
    path('customer/profile/',views.customerProfileView,name='customerprofile'),
    path('customer/profile/edit',views.customerProfileEditView,name='customerprofileedit'),
    path('customer/mediatordetail/<int:pk1>/<int:pk2>/',views.customerMediatorDetailView,name='customermediatordetail'),
    path('customer/history/',views.customerHistoryView,name='customerhistory'),
    path('customer/ratemediator/<int:pk1>/<int:pk2>/',views.rateMediatorView,name='ratemediator'),
    path('customer/notifications',views.customerNotificationsView,name='customernotifications'),
    path('customer/chats/<int:pk1>/<int:pk2>/',views.customerChatsView,name='customerchats'),
    path('customer/rejectedlist',views.customerRejectedView,name='customersrejected'),
    path('customer/completedlist',views.customerCompletedView,name='customerscompleted'),
    path('customer/cancelledlist',views.customerCancelledView,name='customerscancelled'),


    path('customer/cancelconnection/<int:pk>',views.cancelConnectionView,name='cancelconnectioncustomermediator'),
    path('connectcutomermediator/<int:pk1>/<int:pk2>/',views.connectCustomerMediator,name='connectcustomermediator'),
    path('acceptcustomermediator/<int:pk1>/<int:pk2>/',views.acceptCustomerMediator,name='acceptcustomermediator'),
    path('rejectcustomer/<int:pk1>/<int:pk2>/',views.rejectCustomerView,name='rejectcustomer'),
    path('completeconnection/<int:pk1>/<int:pk2>/',views.completeConnectionView,name='completeconnection'),


    
    url(r'^mediator/$',views.mediatorIndexView,name='mediatorindex'),
    url(r'^mediatorlogin/$', views.mediatorLoginView,name='mediatorlogin'),
    url(r'^mediatorlogout/$', views.mediatorLogoutView,name='mediatorlogout'),
    url(r'^mediatorsignup/$',views.mediatorSignupView,name='mediatorsignup'),
    path('mediator/profile/',views.mediatorProfileView,name='mediatorprofile'),
    path('mediator/profile/edit',views.mediatorProfileEditView,name='mediatorprofileedit'),
    path('mediator/history/',views.mediatorHistoryView,name='mediatorhistory'),
    path('mediator/notifications',views.mediatorNotificationsView,name='mediatornotifications'),
    path('mediator/reviews',views.mediatorReviewsView,name='mediatorreviews'),
    path('mediator/chats/<int:pk1>/<int:pk2>/',views.mediatorChatsView,name='mediatorchats'),
    path('mediator/requestslist/',views.mediatorRequestsView,name='mediatorsrequests'),
    path('mediator/acceptedlist/',views.mediatorAcceptedView,name='mediatorsaccepted'),
    path('mediator/rejectedlist/',views.mediatorRejectedView,name='mediatorsrejected'),
    path('mediator/completedlist/',views.mediatorCompletedView,name='mediatorscompleted'),
    path('mediator/cancelledlist/',views.mediatorCancelledView,name='mediatorscancelled'),

]