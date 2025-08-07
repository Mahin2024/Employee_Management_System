import json
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .serializers import createRoomSerializer,getRoomSerializer,createChatSerializer,getChatSerializer,createReportSerializer,getReportSerializer
from .models import Room,Participants,Conversation,Report
from core.permissions import ProfileIsAuthenticated
from rest_framework.response import Response

def index(request):
    return render(request, "chat/index.html")

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})

class createRoomViewset(ModelViewSet):
    http_method_names=['post','get']
    serializer_class= createRoomSerializer
    permission_classes = [ProfileIsAuthenticated]
    queryset=Room.objects.all()

    def get_serializer_context(self):
        user = self.request.user
        participant_ids= self.request.data.get('participant_ids')
        print(participant_ids)
        return {'owner_id':user.id,'participant_ids':participant_ids}

class getRoom(ModelViewSet):
    http_method_names=['get']
    serializer_class=getRoomSerializer
    # queryset=Participants.objects.all()

    def get_queryset(self):
        uuid = self.request.data.get('uuid')
        room = Room.objects.filter(uuid=uuid).first()
        participants=Participants.objects.filter(room_id=room.id)
        print("working", participants)
        return participants


class createChatViewset(ModelViewSet):
    http_method_names=['post']
    serializer_class = createChatSerializer
    permission_classes = [ProfileIsAuthenticated]

    
    def get_serializer_context(self):
        user =self.request.user
        uuid=self.request.data.get('uuid')
        return {'sender':user,'uuid':uuid}
    

class getChatViewset(ModelViewSet):
    http_method_names = ['get']
    serializer_class = getChatSerializer

    def get_queryset(self):
        uuid=self.kwargs.get('uuid')
        room = Room.objects.get(uuid=uuid)
        return Conversation.objects.filter(room=room)
    
class createReportViewset(ModelViewSet):
    http_method_names=['post']
    serializer_class = createReportSerializer
    permission_classes = [ProfileIsAuthenticated]

    def get_serializer_context(self):
        user =self.request.user
        remark=self.request.data.get('remark')

        return {'employee':user,'remark':remark}
    
class getReportViewset(ModelViewSet):
    http_method_names=['get']
    serializer_class = getReportSerializer
    permission_classes = [ProfileIsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        ids= self.request.query_params.get('id')
        # id = json.loads(ids)
        # print(ids,"jdfhdj")
        # for i in ids:
        employee = Report.objects.filter(employee__team_leader=user.id,employee_id=ids)
        return employee

                       