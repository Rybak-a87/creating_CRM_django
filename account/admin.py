from django.contrib import admin

from .models import Account


# admin.site.register(Account)
@admin.register(Account)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {'fields': ('email', 'password1', 'password2',
                           'first_name', 'last_name'),
                'classes': ('wide',)}),
    )
    list_display = ("__str__", "last_name", "is_active")
