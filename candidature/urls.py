from django.urls import path
from .views import save_candidature

urlpatterns = [
    path('<int:pk>/', save_candidature, name='save_candidature'),
]
