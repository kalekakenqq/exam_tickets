from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_form, name='feedback_form'),
    path('thanks/', views.thank_you, name='thank_you'),
]
