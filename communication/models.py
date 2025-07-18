from django.db import models
from core.models import CommonFields
from employee.models import Employee

class Report(CommonFields):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='employee_report')
    remark = models.CharField()
    date = models.DateTimeField()
    
    def __str__(self):
        return self.employee.name
    
    class Meta:
        verbose_name_plural = "Report"


class Conversation(CommonFields):
    sender = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='receiver')
    message = models.CharField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.name
    
    class Meta:
        verbose_name_plural = "Chat"