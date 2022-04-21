from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class UserAdminCustom(UserAdmin):
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'is_superuser',
        'is_staff',
        'is_active',
        'is_student',
        'id_college'
    ]

    search_fields = ['username', 'email', 'id_college']
    readonly_fields = ['date_joined', 'last_login']

    filter_horizontal = []
    list_filter = ['is_student']

    fieldsets = (
        (None, {
            "fields": (
                'username', 'email', 'password', 'first_name', 'last_name', 'id_college')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_student')}),
        ('Personal', {'fields': ('date_joined', 'last_login')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name',
                       'id_college', 'is_staff', 'is_active', 'is_superuser', 'is_student')
            }
        ),
    )

admin.site.register(User, UserAdminCustom)
