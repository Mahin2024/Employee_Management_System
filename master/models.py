from django.db import models
from core.models import CommonFields

class Company(CommonFields):
    name = models.CharField()
    website = models.URLField(null=True,blank=True)
    branch = models.CharField(null=True,blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Company"


class Department(CommonFields):
    type = models.CharField(choices=[
        ('IT','IT'),
        ('Sales','Sales'),
        ('Marketing','Marketing'),
        ('HR','HR'),
    ])
    company = models.ForeignKey(Company,on_delete=models.CASCADE,related_name='company_dept',null=True,blank=True)

    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name_plural = "Department"


class Role(CommonFields):
    type = models.CharField(choices=[
        ('intern','intern'),
        ('Backend Developer','Backend Developer'),
        ('HR Manager','HR Manager'),
        ('Frontend Developer','Frontend Developer'),
        ('SEO','SEO'),
        ('Sales Manager','Sales Manager'),            
        ])
    salary = models.CharField(null=True,blank=True)
    entry = models.TimeField()
    exit = models.TimeField()

    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name_plural = "Role"


class LeavePolicy(CommonFields):
    type = models.CharField(max_length=20, choices=[
        ('Sick', 'Sick Leave'),
        ('Casual', 'Casual Leave'),
        ('Paid', 'Paid Leave'),        
    ], default='Paid')
    description = models.CharField(null=True, blank=True)
    leave_count = models.CharField(null=True,blank=True)

    def __str__(self):
        return self.type
    
    class Meta:
        verbose_name_plural = "Leave Policy"