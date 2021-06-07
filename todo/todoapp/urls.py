from django.urls import path,include
from.views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
rounter=DefaultRouter()
rounter.register("adminregister", adminesgister,basename='adminregister')
rounter.register('userresgister', useresgister , basename='userregister')
rounter.register('todo/api', tasklist, basename='todoapi')
rounter.register('todocreate/api', todocreate, basename='todocreate')
rounter.register('todoretrieve/api', todoretrieve, basename='todoretrieve')
rounter.register('todoput/api', todoput, basename='todoput')
rounter.register('tododelete/api', tododelete, basename='tododelete')


urlpatterns = [
    path("", include(rounter.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tokenencoded', tokenencoded.as_view(),name='tokenencoded')


    ]