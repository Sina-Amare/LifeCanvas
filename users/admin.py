from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_of_birth',
                    'created_at', 'is_staff')
    list_filter = ('is_staff', 'created_at')
    search_fields = ('email', 'username')

# the simpler way :
# admin.site.register(CustomUser)
