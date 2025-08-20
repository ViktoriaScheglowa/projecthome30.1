
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from training.views import CourseViewSet
from user.views import UserCreateAPIView, CustomTokenObtainPairView
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
      public=True,
      permission_classes=[permissions.AllowAny,],
)

router = DefaultRouter()
router.register('', CourseViewSet, basename='courses')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('user/', include('user.urls', namespace='user')),
    path('training/', include('training.urls', namespace='training')),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CustomTokenObtainPairView.as_view(), name='token_refresh'),
    path('register/', UserCreateAPIView.as_view(), name='register'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
