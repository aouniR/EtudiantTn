from django.urls import path
from .views import offer_list

urlpatterns = [
    path('', offer_list, name='offer_list'),
]