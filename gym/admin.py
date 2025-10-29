# admin.py
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

class FeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'Fee', 'Actualfee', 'Pendingfee', 'Datetime')
    list_filter = ('user',)
    search_fields = ('user__username', 'Fee', 'Actualfee','Pendingfee')

    def save_model(self, request, obj, form, change):
       
        if obj.Actualfee is not None and obj.Fee is not None:
            obj.Pendingfee = obj.Fee - obj.Actualfee
            if obj.Pendingfee < 0:
                obj.Pendingfee = 0
        else:
            obj.Pendingfee = 0
            
       
        if not obj.user_id and request.user.is_authenticated:
            obj.user = request.user
            
        
        super().save_model(request, obj, form, change)
    
class attendanceadmin(admin.ModelAdmin):
    list_display =('user','month',"attendance_date",'status')
    list_filter = ('user',)
    search_fields = ('user__username', 'month')


admin.site.register(fee, FeeAdmin)
admin.site.register(Attendance,attendanceadmin)
admin.site.register(Product)
