from django.urls import path
from .views import rec_dashboard,add_offer
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   path('Dashboard/',rec_dashboard,name='rec_dashboard'),
   path('add_offer/',add_offer,name='add_offer'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)