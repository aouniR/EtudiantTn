from django.urls import path
from .views import register_student, registration_confirmation,register_recruiter,user_login,register,user_logout

urlpatterns = [
    path('register_student/', register_student, name='register_student'),
    path('register/', register, name='register'),
    path('register_recruiter/', register_recruiter, name='register_recruiter'),
    path('registration_confirmation/', registration_confirmation, name='registration_confirmation'),
    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login')
]
