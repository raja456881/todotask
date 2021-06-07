from rest_framework.decorators import api_view
from .models import User
from .searilizers import *
from rest_framework.response import  Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from django.conf import settings
import jwt
#Api all todolist Details ,  authentication and access only admin and user
class tasklist(viewsets.ViewSet):
    def list(self, request):
        try :
            if request.user.is_authenticated or request.user.is_admin==True:
                querset=todoiteam.objects.all()
                serializers=todosearilizers(querset, many=True)
                return Response(serializers.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
#Api create todolist , acress only admin
class todocreate(viewsets.ViewSet):
    def create(self, request):
        try :
            if request.user.is_admin:
               searilizers=todosearilizers(data=request.data, context={'request': request})
               if searilizers.is_valid():
                   searilizers.save()
                   return Response( searilizers.data, status=status.HTTP_201_CREATED)
               else:
                  return Response(searilizers.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
                return Response({'msg': 'user is not admin'},status=status.HTTP_401_UNAUTHORIZED)


#Api get only one todo iteam  acress only admin
class todoretrieve(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        try:
            if request.user.is_admin:
                id=pk
                if id is not  None:
                    todo=todoiteam.objects.get(id=id)
                    serializers=todosearilizers(todo)
                    return Response(serializers.data, status=status.HTTP_200_OK)
                else:
                    return Response( {'msg': "ID  is not exits" }, status=status.HTTP_400_BAD_REQUEST )
        except :
               return Response({'msg': 'user is not admin'},status=status.HTTP_401_UNAUTHORIZED)
#Api update only one todo iteam  acress only admin
class todoput(viewsets.ViewSet):
    def update(self, request, pk=None):
        try :
            if request.user.is_admin:
                id=pk
                if id is not None:
                    todo = todoiteam.objects.get(id=id)
                    serializers = todosearilizers(todo, data=request.data)
                    if serializers.is_valid():
                        serializers.save()
                        return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
                    else:
                        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'msg': "ID  is not exits" }, status=status.HTTP_400_BAD_REQUEST )
        except:
            return Response({'msg': 'user is not admin'},status=status.HTTP_401_UNAUTHORIZED)
#Api delete only one todo iteam  acress only admin
class tododelete(viewsets.ViewSet):
    def destroy(self, request, pk):
        try:
            if request.user.is_admin:
                id = pk
                todo = todoiteam.objects.get(id=id)
                todo.delete()
                return Response({'masg': "Delete successful"}, status=status.HTTP_200_OK)
        except:
            return Response({'msg': 'user is not admin'}, status=status.HTTP_401_UNAUTHORIZED)








#Api for admin register
class adminesgister(viewsets.ViewSet):
    def create(self, request):
        searilizers=adminsearilizers(data=request.data)
        if searilizers.is_valid(raise_exception=True):
            searilizers.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(searilizers.errors, status=status.HTTP_400_BAD_REQUEST)
#Api for user register
class useresgister(viewsets.ViewSet):
    def create(self, request):
        searilizers=usersearilizers(data=request.data)
        if searilizers.is_valid(raise_exception=True):
            searilizers.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(searilizers.errors, status=status.HTTP_400_BAD_REQUEST)

#Api for encoded token give details for user
class tokenencoded(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        token = request.GET.get('token')
        print('payload ' + str(settings.SECRET_KEY))
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            print('payload 1 ' + str(payload))
            user = User.objects.get(id=payload['user_id'])
            return Response({'first_name': user.first_name , 'last_name': user.last_name,
                             'email': user.email, 'IsActiva': user.is_active, 'Roles': user.is_roles}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            return Response({'error': 'Activations link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)