from django.urls import path
from home import views


urlpatterns = [
    path('', views.Home, name='Home'),
    path('Signup', views.Signup, name='Signup'),
    path('Otp/<str:phone>,<int:id>', views.Otp, name='Otp'),
    path('Login', views.Login, name='Login'),
    path('Logout', views.Logout, name='Logout'),
    path('Forget_pass', views.Forget_pass, name='Forget_pass'),
    path('reset_pass/<str:phone>/<int:id>/', views.Reset_pass, name='reset_pass')
]
