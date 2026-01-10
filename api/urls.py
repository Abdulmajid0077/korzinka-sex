from django.urls import path
from .views import dashboard, login


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('login/', login, name='login'),
]