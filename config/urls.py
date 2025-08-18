
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from training.views import CourseViewSet
from user.views import UserCreateAPIView, CustomTokenObtainPairView

router = DefaultRouter()
router.register('', CourseViewSet, basename='courses')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('user/', include('user.urls', namespace='user')),
    path('training/', include('training.urls', namespace='training')),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CustomTokenObtainPairView.as_view(), name='token_refresh'),
    path('register/', UserCreateAPIView.as_view(), name='register')

]
