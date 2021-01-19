from django.conf.urls import url
from . import views
# from django.contrib.auth import views as auth_views


app_name='customer'

urlpatterns=[
    url(r'^$',views.IndexView.as_view(),name='index'),
    url(r'^login/$', views.customerLoginView,name='login'),
    url(r'^logout/$', views.customerLogoutView,name='logout'),
    url(r'^signup/$',views.customerSignupView,name='signup'),
]