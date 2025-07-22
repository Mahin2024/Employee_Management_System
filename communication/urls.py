from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

urlpatterns = [
    path('',include(router.urls)),
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
]