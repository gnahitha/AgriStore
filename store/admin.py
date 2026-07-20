# Register your models here.
from django.contrib import admin
from .models import Product, Review, Cart, Order, OrderItem, Wishlist

admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Wishlist)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer_name",
        "phone",
        "total_amount",
        "status",
        "created_at",
    )

    list_filter = ("status",)

    search_fields = ("customer_name", "phone")