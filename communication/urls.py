from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import createRoomViewset

router = DefaultRouter()

router.register(r'create',createRoomViewset,basename='createRoom')

urlpatterns = [
    path('',include(router.urls)),
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]