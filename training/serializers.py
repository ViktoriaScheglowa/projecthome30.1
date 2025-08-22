from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from training.models import Course, Lesson, Subscription
from training.validators import LinkVideoValidator


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkVideoValidator(field="video")]


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True)
    is_subscribed = SerializerMethodField()

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course_id=course.pk).count()

    def get_is_subscribed(self, course):
        user = self.context.get("request").user
        return Subscription.objects.filter(user=user, course=course).exists()

    class Meta:
        model = Course
        fields = ('title', 'preview', 'description', 'count_lessons', 'lessons', 'is_subscribed')
        validators = [LinkVideoValidator(field="video")]
