from django.urls import path
from .views import rent_offers

urlpatterns = [
    path('', rent_offers, name='rent_offers'),
]