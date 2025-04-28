from django.contrib import admin
from .models import Journal


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'mood', 'created_at', 'updated_at')
    list_filter = ('mood', 'created_at', 'user')
    search_fields = ('title', 'content', 'user__email')
    ordering = ('-created_at',)
