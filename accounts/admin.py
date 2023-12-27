from django.contrib import admin
from .models import Profile, StudentData

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)

class StudentDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'balance')
    list_filter = ('graduation_year', 'request_status')
    search_fields = ('user__username', 'first_name', 'last_name')
    readonly_fields = ('transaction_history', 'transaction_time')

admin.site.site_header = 'Student Profiles'  # Change admin site header
admin.site.site_title = 'Student Profiles'   # Change title on admin index page

admin.site.register(Profile, ProfileAdmin)
admin.site.register(StudentData, StudentDataAdmin)
