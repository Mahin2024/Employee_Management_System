from django.contrib import admin
from .models import Report,Conversation,Room,Participants

@admin.register(Report)
class registerReport(admin.ModelAdmin):
    list_display=['id','employee','remark','date']

@admin.register(Conversation)
class registerConversation(admin.ModelAdmin):
    list_display=['id','sender','receiver','message','timestamp']

@admin.register(Room)
class registerRoom(admin.ModelAdmin):
    list_display = ['id','name','participant','type','uuid']

@admin.register(Participants)
class registerParticipents(admin.ModelAdmin):
    list_display = ['id','participant','room']