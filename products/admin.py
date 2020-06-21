from django.contrib import admin

from  .models import Category, Tovar, Delivery, Order, OrderProduct

class OrderProductInline(admin.StackedInline):
    model = OrderProduct
    extra = 1
    readonly_fields = ['price', 'summaryprice']
    def price(self, obj):
        return obj.tovar.unit_price
    def summaryprice(self, obj):
        return obj.tovar.unit_price*obj.kol

class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderProductInline]
    readonly_fields = ['id','date', 'allsummaryprice']
    def allsummaryprice(self, obj):
        price = 0
        orderproducts = OrderProduct.objects.filter(order = obj)
        for op in orderproducts:
            price += op.tovar.unit_price*op.kol
        return price

admin.site.register(Category)
admin.site.register(Tovar)
admin.site.register(Delivery)
admin.site.register(Order,OrderAdmin)