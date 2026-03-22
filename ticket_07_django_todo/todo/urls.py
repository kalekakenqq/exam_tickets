from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:pk>/', views.toggle_complete, name='toggle_complete'),
    path('delete/<int:pk>/', views.delete_task, name='delete_task'),
]
