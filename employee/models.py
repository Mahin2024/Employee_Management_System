from django.db import models
from core.models import CommonFields
from master.models import Role, Department,LeavePolicy

class Employee(CommonFields):
    team_leader = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    joining_date=models.DateField()
    name = models.CharField(max_length=25)
    email = models.EmailField(max_length=50,unique=True)
    contact = models.CharField(max_length=10)
    password = models.CharField()
    role = models.ForeignKey(Role,on_delete=models.CASCADE,related_name='role', null=True,blank=True)
    department = models.ForeignKey(Department,on_delete=models.CASCADE, related_name='department',null=True, blank=True)
    image = models.ImageField(upload_to='media/',null=True,blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Employee"
        

class Attendance(CommonFields):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='employee_attendace')
    date = models.DateField()
    status= models.CharField(choices=[
        ('present','present'),
        ('absent','absent'),
        ('half_day','half_day'),
    ],default='absent')
    checkin = models.TimeField(null=True,blank=True)
    checkout = models.TimeField(null=True,blank=True)
    is_late = models.BooleanField(default=False)
    is_early = models.BooleanField(default=False)
    location=models.CharField(choices=[("WFH","WFH"),
                                       ("WFO","WFO"),
                                       ],null=True,blank=True)

    def __str__(self):
        return self.employee.name
    
    class Meta:
        verbose_name_plural = "Attendance"

# salary- employee(fk), role(fk), amount, bonus, attendance(fk), deductions, net_salary
class Salary(CommonFields):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='employee_salary')
    month = models.CharField(null=True,blank=True)
    amount = models.IntegerField()
    bonus = models.IntegerField(null=True,blank=True)
    deductions = models.IntegerField(null=True,blank=True)
    net_salary = models.IntegerField()

    def __str__(self):
        return self.employee.name
    
    class Meta:
        verbose_name_plural = "Salary"

class Leave(CommonFields):
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='employee_leave')
    policies = models.ForeignKey(LeavePolicy,on_delete=models.CASCADE,related_name='policy')
    status= models.CharField(choices=[
        ('rejected','rejected'),
        ('approved','approved'),
        ('pending','pending'),
    ],default='pending')
    type = models.CharField(choices=[
        ('half_day','half_day'),
        ('full_day','full_day'),
    ])
    start_date = models.DateField()
    end_date = models.DateField()
    is_paid=models.BooleanField(default=False)
    reason = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.employee.name
    
    class Meta:
        verbose_name_plural = "Leave"