from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}  # slug از روی name پر میشه


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'category']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}  # slug از روی name پر میشه
    list_editable = ['price', 'available']
    ordering = ['-created']

    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'slug', 'image', 'description', 'price', 'available')
        }),
        ('Dates', {
            'fields': ('created', 'updated'),
            'classes': ('collapse',),  # این بخش رو جمع شدنی میکنه
        }),
    )

    readonly_fields = ['created', 'updated']