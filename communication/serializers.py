import json
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Room,Participants,Conversation


class createRoomSerializer(ModelSerializer):
    class Meta:
        model=Room
        fields ="__all__"

    def create(self, validated_data):
        owner_id=self.context.get('owner_id')
        validated_data['participant_id'] = owner_id
        room = Room.objects.create(**validated_data)
        print("ow",owner_id)
        Participants.objects.create(room=room,participant_id=owner_id)
        participant_ids = json.loads(self.context.get('participant_ids'))
        print(participant_ids,"djfdifhi")
        for participant in participant_ids:
            participant = Participants.objects.create(room=room,participant_id=participant)
        return room
    

class updateRoomSerializer(ModelSerializer):
    class Meta:
        model=Participants
        fields ="__all__"

class createChatSerializer(ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id','sender','room','message','timestamp','sent','delivered','seen']

    def create(self, validated_data):
        uuid=self.context.get('uuid')
        validated_data['sender']=self.context.get('sender')
        room = Room.objects.get(uuid=uuid)
        chat = Conversation.objects.create(room=room,**validated_data)
        return chat
    
class getChatSerializer(ModelSerializer):
    sender = serializers.CharField(read_only=True)
    class Meta:
        model = Conversation
        fields = ['id','sender','room','message','timestamp','sent','delivered','seen']
