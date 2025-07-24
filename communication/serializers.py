import json
from rest_framework.serializers import ModelSerializer
from .models import Room,Participants



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
    