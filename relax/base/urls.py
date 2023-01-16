from . import views
from django.urls import path

urlpatterns = [
   
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),

    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name="room"),

    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('delete-room/<str:pk>', views.deleteRoom, name='delete-room'),
]
