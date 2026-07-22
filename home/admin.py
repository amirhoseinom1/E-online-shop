from django.contrib import admin
from .models import (
    Category, Product, Comment,
    Cart, CartItem,Order,
    OrderItem,
)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'created_at', 'category']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'available']
    ordering = ['-created_at']

    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'image', 'description', 'price', 'available')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    readonly_fields = ['created_at', 'updated_at']



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__full_name', 'product__name', 'text']
    actions = ['approve_comments', 'reject_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)

    approve_comments.short_description = 'Approve selected comments'

    def reject_comments(self, request, queryset):
        queryset.update(is_active=False)

    reject_comments.short_description = 'Reject selected comments'



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__full_name', 'user__phone_number']



@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'price']
    search_fields = ['product__name']



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'created_at', 'created_by_admin']
    list_filter = ['status', 'created_at', 'created_by_admin']
    search_fields = ['user__full_name', 'user__phone_number']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    search_fields = ['product__name']