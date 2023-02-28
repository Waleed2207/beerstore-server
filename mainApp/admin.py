from django.contrib import admin
from .models import UserProfile, Products, Suppliers, Orders
admin.site.register(UserProfile)
admin.site.register(Products)
admin.site.register(Suppliers)
admin.site.register(Orders)
