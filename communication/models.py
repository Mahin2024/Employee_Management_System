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


class Room(CommonFields):
    name=models.CharField()
    participant = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='employee_participent')
    type =models.BooleanField(choices=[
        ('group','group'),
        ('direct','direct')
    ])
    uuid=models.CharField(unique=True)

    def __str__(self):
        return self.name
   
    class Meta:
        verbose_name_plural = "Room"


class Conversation(CommonFields):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name='room')
    sender = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=True)
    delivered = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    
    def __str__(self):
        return self.sender.name
    
    class Meta:
        verbose_name_plural = "Chat"

class Participants(CommonFields):
    participant = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='participants_participant')
    room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name='participants_room')

    def __str__(self):
        return self.participent.name
    
    class Meta:
        verbose_name_plural = "Participent"