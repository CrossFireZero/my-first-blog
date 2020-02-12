from django.urls import path
from . import views


urlpatterns = [
    path('editor', views.simple, name='code_editor'),
]