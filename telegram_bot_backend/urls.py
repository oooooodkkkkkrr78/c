from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from your_app import views

urlpatterns = [
    path('', views.home, name='home'),
    # ... your other URL patterns ...
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
