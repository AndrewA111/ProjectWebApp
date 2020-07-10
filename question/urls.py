from django.urls import path
from question import views

app_name = 'question'

urlpatterns = [
    path('', views.index, name='index')
]