from django.urls import path
from .views import register_user, emergency_info

urlpatterns = [
    path('', register_user, name='home'),
    path('register/', register_user, name='register'),
    path('emergency/<uuid:user_id>/', emergency_info, name='emergency_info'),
]
