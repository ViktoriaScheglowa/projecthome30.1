from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from user.models import User, Pay
from user.serializers import UserSerializers, PaySerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()


class UserRetrieveAPIView(LoginRequiredMixin, RetrieveAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return self.queryset
        else:
            raise PermissionDenied


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()


class PayViewSet(ListAPIView):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('lesson', 'course', 'form_of_payment')
    ordering_fields = ('payment_date',)
