from django.contrib import admin
from django.urls import include, path, re_path
from qnamit import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Opis API projektu",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kontakt@twojemail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('qna/', include('qna.urls')),
    path('qna-rest/v1/api/', include('qna_rest.urls')),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
      urlpatterns += [
          path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
          path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
          re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
      ]
