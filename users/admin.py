

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Display these fields in the user list view
    list_display = ('username', 'email', 'first_name', 'last_name','is_viewer', 'is_journalist', 'is_editor', 'is_head', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-username',)

    # Define the fields to be displayed in the user detail view
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff','is_viewer', 'is_superuser', 'is_journalist', 'is_editor', 'is_head')}),
    )

    # Define the fields to be displayed when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2','is_viewer', 'is_journalist', 'is_editor', 'is_head'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # if it's a new user, set the default role
            obj.is_journalist = True
        super().save_model(request, obj, form, change)
admin.site.register(CustomUser,CustomUserAdmin)

admin.site.register(UserProfile)
admin.site.register(Category)

