from django.contrib import admin
from .models import Category, Product, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'category']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'available']
    ordering = ['-created']

    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'image', 'description', 'price', 'available')
        }),
        ('Dates', {
            'fields': ('created', 'updated'),
        }),
    )

    readonly_fields = ['created', 'updated']



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created', 'is_active']
    list_filter = ['is_active', 'created']
    search_fields = ['user__full_name', 'product__name', 'text']
    actions = ['approve_comments', 'reject_comments']

    def approve_comments(self, request, queryset):
        queryset.update(is_active=True)

    approve_comments.short_description = 'Approve selected comments'

    def reject_comments(self, request, queryset):
        queryset.update(is_active=False)

    reject_comments.short_description = 'Reject selected comments'
