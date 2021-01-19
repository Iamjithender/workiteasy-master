from django.contrib import admin

# Register your models here.

from .models import User,CustomerInfo,MediatorInfo,Connect,Reviews,NotAvailableDates,Chats,Messages
# ,Connect

admin.site.register(User)
admin.site.register(CustomerInfo)
admin.site.register(MediatorInfo)
admin.site.register(Connect)
admin.site.register(Reviews)
admin.site.register(NotAvailableDates)
admin.site.register(Chats)
admin.site.register(Messages)