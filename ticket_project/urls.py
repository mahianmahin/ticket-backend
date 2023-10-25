from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from api.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hero_image/', hero_image),
    path('packages/', packages),
    path('package/<str:req_status>/<int:tag>/', package),
    path('register/', user_register),
    path('code/', qrcode),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('create_checkout_session/', create_checkout_session, name='create_checkout_session')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)