from django.contrib import admin
from  scorptec.models import UserDetail, Category, Product,Order,OrderProduct, Favourite
# Register your models here.
admin.site.register(UserDetail)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Favourite)
