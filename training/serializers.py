from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from training.models import Course, Lesson
from training.validators import LinkVideoValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkVideoValidator(field="video")]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(many=True, source='lesson_set')

    def get_count_lessons(self, course):
        return Lesson.objects.filter(course_id=course.pk).count()

    class Meta:
        model = Course
        fields = ('title', 'preview', 'description', 'count_lessons', 'lessons')
        validators = [LinkVideoValidator(field="video")]
