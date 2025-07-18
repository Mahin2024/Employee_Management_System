from django.contrib import admin
from .models import Company,Department,Role,LeavePolicy
# Register your models here.

@admin.register(Company)
class registerCompany(admin.ModelAdmin):
    list_display = ['id','name','website','branch']

@admin.register(Department)
class registerDepartment(admin.ModelAdmin):
    list_display = ['id','type','company']

@admin.register(Role)
class registerRole(admin.ModelAdmin):
    list_display = ['id','type','salary','entry','exit']

@admin.register(LeavePolicy)
class registerLeavePolicy(admin.ModelAdmin):
    list_display = ['id','type','description','leave_count']

    
