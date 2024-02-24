"""
URL configuration for EtudiantTn project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')), 
    path('profile/', include('dashboard.urls')),
    path('offers/', include('offers.urls')),
    path('unauthorizedUsers/', include('unauthorizedUsers.urls')),
    path('news/', include('news.urls')),
    path('settings/', include('settings.urls')),
    path('candidature/',include('candidature.urls')),
    path('rent/',include('rent.urls')),
    path('tests/',include('tests.urls')),
    path('recruiter/profile/',include('dashboard.urls_recruiter')),
    re_path(r'^(?!media/|static/).*$', RedirectView.as_view(pattern_name='login', permanent=False), name='catch-all')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
