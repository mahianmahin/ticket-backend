from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hero_image/', hero_image),
    path('packages/', packages),
    path('package/<str:req_status>/<int:tag>/', package),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)