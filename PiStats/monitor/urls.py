from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),               # The main dashboard page
    path('api/stats/', views.system_stats, name='stats'),

]