from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from requests import Response
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from user.models import User, Pay
from user.serializers import UserSerializers, PaySerializer, UserPublicSerializer
from user.services import check_payment_status, create_stripe_sessions, convert_to_dollars, create_stripe_price


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_summary="Создание пользователя",
        operation_description="Создание нового пользователя. Для авторизации требуются email и пароль.",
    ),
)
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_summary="Список пользователей",
        operation_description="Вывод списка авторизованных пользователей. Требуется авторизация. Для просмотра доступны "
        "поля: email, имя, город, аватар.",
        responses={200: UserPublicSerializer(many=True)},
    ),
)
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


class PayListView(ListAPIView):
    queryset = Pay.objects.all()
    serializer_class = PaySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('lesson', 'course', 'form_of_payment')
    ordering_fields = ('payment_date',)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        amount_in_dollars = convert_to_dollars(payment.amount)
        price = create_stripe_price(amount_in_dollars)
        session_id, payment_link = create_stripe_sessions(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

    @action(detail=True, methods=["get"])
    def check_status(self, request, pk=None):
        """Проверка статуса оплаты."""
        payment = self.get_object()
        if not payment.session_id:
            return Response({"error": "Неверный ID платежа."}, status=400)

        status_info = check_payment_status(payment.session_id)
        payment.payment_status = status_info.get(
            "payment_status", payment.payment_status
        )
        payment.save()

        return Response(
            {"payment_id": payment.id,
             "status": payment.payment_status,
             "details": status_info,
            }
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)


class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = (AllowAny,)


