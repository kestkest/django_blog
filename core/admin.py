from image_cropping import ImageCroppingMixin

from django.contrib.auth.admin import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.urls import views

from .models import User as MyUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
# admin.site.unregister(MyUser)


class MyUserAdmin(ImageCroppingMixin, UserAdmin):
    model = MyUser
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'slug', 'username', 'password')}),
        ('Personal info', {'fields': (
                                      'first_name',
                                      'last_name',
                                      'avatar',
                                      'avatar_cropping',
                                      'about',
                                      'email_visible',
                                      'birth_date',
                                      )
                           }
         ),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'about'),
        }),
    )


admin.site.register(MyUser, MyUserAdmin)
