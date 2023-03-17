from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('<int:pk>',views.index,name='index'),
    path('get_messages/',views.get_messages,name='get_messages'),
    path('get_chat/',views.get_chat,name='get_chat'),
    path('get_users/',views.get_users,name='get_chat'),
]
