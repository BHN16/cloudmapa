from django.urls import path
from . import views

urlpatterns = [
    path('map/', views.map_view, name='map_view'),
    path('universal/', views.universal_view, name='universal_view'),
]
