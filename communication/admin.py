from django.contrib import admin
from .models import Report,Conversation

@admin.register(Report)
class registerReport(admin.ModelAdmin):
    list_display=['id','employee','remark','date']

@admin.register(Conversation)
class registerConversation(admin.ModelAdmin):
    list_display=['id','sender','receiver','message','timestamp']