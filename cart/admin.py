from django.contrib import admin

from cart.models import Cart,Cartitem,Orders,OrderProduct,Payment




admin.site.register(Orders)
admin.site.register(OrderProduct)
admin.site.register(Payment)


admin.site.register(Cart)
admin.site.register(Cartitem)