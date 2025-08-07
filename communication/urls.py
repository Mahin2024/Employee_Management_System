from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from .views import createRoomViewset,getRoom,createChatViewset,getChatViewset,createReportViewset,getReportViewset

router = DefaultRouter()

router.register(r'create',createRoomViewset,basename='createRoom')
router.register(r'getRoom',getRoom,basename='getRoom')
router.register(r'chat',createChatViewset,basename='createChat')
router.register(r'report',createReportViewset,basename='report')
router.register(r'getReport',getReportViewset,basename='getReport')



urlpatterns = [
    path('',include(router.urls)),
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("roomchat/<str:uuid>/", getChatViewset.as_view({'get': 'list'}), name="Chat"),
]