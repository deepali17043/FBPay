from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'name', 'Birthday', 'email']
    list_filter = ()
    model = User
    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)