from django.contrib import admin
from .models import ParentProfile

class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'parent_first_name', 'parent_last_name', 'child_username', 'parent_wallet')
    list_filter = ('parent_first_name', 'parent_last_name', 'child_username')
    search_fields = ('user__username', 'parent_first_name', 'parent_last_name', 'child_username')
    readonly_fields = ('created_at',)

admin.site.register(ParentProfile, ParentProfileAdmin)
