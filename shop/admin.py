from django.contrib import admin

from .models import Category, Order, OrderItem, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_hit', 'is_spicy', 'available']
    list_filter = ['category', 'is_hit', 'available']
    list_editable = ['price', 'is_hit', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'delivery', 'payment', 'paid', 'created']
    list_filter = ['delivery', 'payment', 'paid', 'created']
    search_fields = ['name', 'phone']
    inlines = [OrderItemInline]
