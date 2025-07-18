from rest_framework import serializers
from .models import Employee,Leave

class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

class employeeSerializar(serializers.ModelSerializer):
    role = serializers.CharField(read_only = True)
    department = serializers.CharField(read_only = True)

    class Meta:
        model = Employee
        fields = "__all__"
        read_only_fields=['id','team_leader','joining_date','password','role','department']

class leaveSerializer(serializers.ModelSerializer):
    employee = serializers.CharField(read_only =True)

    class Meta:
        model = Leave
        fields =['id','employee','policies','type','status','start_date','end_date','is_paid','reason']

class leaveStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model= Leave
        fields =['id','employee','policies','type','status','start_date','end_date','is_paid','reason']
        read_only_fields=['id','employee','policies','type','start_date','end_date','is_paid','reason']

class paidLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields =['id','employee','policies','type','status','start_date','end_date','is_paid','reason']

