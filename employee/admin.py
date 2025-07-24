from django.contrib import admin
from .models import Employee,Attendance,Salary,Leave
from django.contrib.auth.hashers import make_password
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter

@admin.register(Employee)
class registerEmployee(admin.ModelAdmin):
    list_display=['id','name','team_leader','joining_date','email','contact','role','department','image']
    list_display_links = ('name',)
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password') and not change:
            obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


@admin.register(Attendance)
class registerAttendance(admin.ModelAdmin):
    list_display=['id','employee','date','status','checkin','checkout','is_early','is_late','location']
    list_filter = ('employee', RelatedDropdownFilter),
    search_fields = (
        "location",
        "status",
    )

@admin.register(Salary)
class registerAttendance(admin.ModelAdmin):
    list_display=['id','employee','amount','bonus','deductions','net_salary']

@admin.register(Leave)
class registerLeave(admin.ModelAdmin):
    list_display=['id','employee','policies','type','status','start_date','end_date','is_paid','reason']