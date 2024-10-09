from django.urls import path
from user_login import views

urlpatterns = [
    path('login/',views.UserLogin.as_view(),name='login')
]