
from django.contrib import admin
from django.urls import path, include

from user.views import UserCreateAPIView, CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls', namespace='user')),
    path('training/', include('training.urls', namespace='training')),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CustomTokenObtainPairView.as_view(), name='token_refresh'),
    path('register/', UserCreateAPIView.as_view(), name='register')

]
