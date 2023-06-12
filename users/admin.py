from users.models import Organization, User

from django.contrib import admin
from .forms import CustomUserCreationForm


class UserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    ordering = ['id']
    fields = [
        'email',
        'organization',
        'first_name',
        'last_name',
        'is_active',
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Organization)
