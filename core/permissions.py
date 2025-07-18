from rest_framework.permissions import BasePermission
from core.authentication import decode_token
from employee.models import Employee
from employee.serializers import employeeSerializar
from rest_framework.exceptions import NotAuthenticated

class ProfileIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        response = decode_token(request,Employee,employeeSerializar)
        if response.status_code == 200:
            user_id = response.data['id']
            user = Employee.objects.filter(id=user_id).first()
            request.user = user
            request.id = user_id
            return True
        else:
            # Raise exception to properly block access
            raise NotAuthenticated(response.data.get("error"))
