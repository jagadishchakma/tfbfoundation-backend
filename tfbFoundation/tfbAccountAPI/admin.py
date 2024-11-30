from django.contrib import admin
from .models import Profile


#---------- USER PROFILE ADMIN START ----------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_no', 'profession', 'account_type','created_at')
#---------- USER PROFILE ADMIN END ----------



