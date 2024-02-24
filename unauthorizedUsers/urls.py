from django.urls import path
from .views import my_protected_view,error_cand_view

urlpatterns = [
    path('', my_protected_view, name='my_protected_view'),
    path('error_cand', error_cand_view, name='error_cand'),
]
