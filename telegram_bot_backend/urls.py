from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from tradingview import views  # Import views from the tradingview app

urlpatterns = [
    path('', views.home, name='home'),  # Add this line for the root URL
    path('admin/', admin.site.urls),
    path('webhooks/', include('tradingview.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
