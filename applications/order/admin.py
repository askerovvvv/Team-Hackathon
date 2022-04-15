from django.contrib import admin

from applications.order.models import *

admin.site.register(Status)
admin.site.register(Order)
# admin.site.register(OrderItem)

