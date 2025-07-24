from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import createRoomSerializer
from .models import Room
from core.permissions import ProfileIsAuthenticated

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

        

