from django.urls import path
from categories import views

urlpatterns = [
    path('Formals', views.Formals,name='Formals'),
    path('Casuals', views.Casuals,name='Casuals'),
    path('Boots', views.Boots,name='Boots'),
    path('Weddings', views.Weddings,name='Weddings'),
    path('Slippers', views.Slippers,name='Slippers'),
    
]