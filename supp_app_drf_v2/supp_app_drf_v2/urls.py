from django.contrib import admin
from django.urls import path, include, re_path
from supp_app_drf_v2.yasg import urlpatterns as doc_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('drf-auth/', include('rest_framework.urls')),
    path('api/v1/', include('support.urls')),
]


# Swagger
urlpatterns += doc_urls


# Django debug toolbar
urlpatterns += path('__debug__/', include('debug_toolbar.urls')),


# Djoser
urlpatterns += [
    path('api/v1/auth_djoser/', include('djoser.urls')),
    re_path(r'^auth_djoser/', include('djoser.urls.authtoken')),
]


# JWT
urlpatterns += [
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
