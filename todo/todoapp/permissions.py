from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
class listapipermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return Response(status=status.HTTP_401_UNAUTHORIZED)
