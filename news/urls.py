from django.urls import path
from .views import news,detail_news,previous_news,next_news
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   path('',news,name='news'),
   path('<int:pk>/', detail_news, name='detail_news'),
   path('#-/<int:pk>/', previous_news, name='previous_news'),
   path('#+/<int:pk>/', next_news, name='next_news'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)