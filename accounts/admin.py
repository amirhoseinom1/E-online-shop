from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, Comment
from django.contrib.auth.models import Group


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



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        ('Main', { 'fields': ('email', 'phone_number', 'full_name', 'password') }),
        ('Permissions', { 'fields': ('is_active', 'is_admin', 'last_login') }),
    )

    add_fieldsets = (
        (None, { 'fields': ('phone_number', 'email','full_name', 'password1', 'password2') }),
    )

    search_fields = ('email', 'full_name')
    ordering = ('full_name',)
    filter_horizontal = ()

admin.site.unregister(Group)
admin.site.register(User, UserAdmin)