import generics
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from training.models import Course, Lesson, Subscription
from training.paginators import CustomPaginator
from training.permissions import IsOwner
from training.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from user.permissions import IsModer


class CourseViewSet(viewsets.ModelViewSet):
    # serializer_class = CourseDetailSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPaginator

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if getattr(self, 'swagger_fake_view', False):
            return Course.objects.none()
        if not self.request.user.groups.filter(name='manager').exists():
            qs = qs.filter(owner=self.request.user)
        return qs

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = (IsAuthenticated, ~IsModer,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsAuthenticated, IsModer | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (IsAuthenticated, ~IsModer | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPaginator

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.groups.filter(name='manager').exists():
            qs = qs.filter(owner=self.request.user)
        return qs


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, ~IsModer | IsOwner,)


class SubscriptionAPIView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
        return Response({"message": message})
