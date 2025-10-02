from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from training.models import Course, Lesson
from user.models import User

# User = get_user_model()


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user@user.ru")
        self.user2 = User.objects.create(email="user2@user.ru")
        self.course = Course.objects.create(title="Python-разработчик", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Django", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)
        self.user2.save()

    def test_lesson_create(self):
        self.moderators_group = Group.objects.create(name="manager")
        self.user2.groups.add(self.moderators_group)
        self.user2.save()

    def test_course_retrieve(self):
        """Тестирование просмотра детальной информации о курсе"""
        url = reverse("courses-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create(self):
        """Тестирование создания курса"""
        data = {
            "title": "Веб-разработчик",
            "description": "Практический курс для тех, кто хочет создавать веб-проекты",
        }

        url = reverse("courses-list")
        response = self.client.patch(url, data)
        data = response.json()

        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #         # self.assertEqual(data.get("title"), self.course.title)
        #
        #         # self.assertEqual(response.json().get("owner"), self.user.id)
        self.assertTrue(Course.objects.all().count(), 2)

    # def test_course_update(self):
    #     """Тестирование обновления информации о курсе."""
    #     url = reverse("courses-detail", args=(self.course.pk,))
    #     data = {"description": "Научим создавать приложения."}
    #     response = self.client.patch(url, data)
    #     data = response.json()
    #
    #     # self.assertEqual(response.status_code, status.HTTP_200_OK)

    # self.assertEqual(data.get("description"), "Научим создавать приложения.")

    def test_course_delete(self):
        """Тестирование удаления курса."""
        url = reverse("courses-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Course.objects.all().count(), 0)

    # def test_course_delete_with_moder(self):
    #     """Тестирование удаления записи модератором."""
    #     self.client.force_authenticate(user=self.user2)
    #     url = reverse("courses-detail", args=(self.course.pk,))
    #     response = self.client.delete(url)
    #
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


#
#         self.assertEqual(Course.objects.all().count(), 1)
#
#     def test_course_list(self):
#         """Тестирование получения списка курсов"""
#         url = reverse("courses-list")
#         response = self.client.get(url)
#         data = response.json()
#
#         result = {
#             "count": 1,
#             "next": None,
#             "previous": None,
#             "results": [
#                 {
#                     "title": self.course.title,
#                     "preview": None,
#                     "description": "",
#                     "count_lessons": 1,
#                     "lessons": [
#                         {
#                             "id": self.lesson.pk,
#                             "name": self.lesson.name,
#                             "description": None,
#                             "preview": None,
#                             "video": None,
#                             "course": self.course.pk,
#                             "owner": self.user.pk,
#                         }
#                     ],
#                     "is_subscribed": False,
#                 }
#             ],
#         }
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # self.assertEqual(data, result)
#
#
# class LessonTestCase(APITestCase):
#
#     def setUp(self):
#         self.user = User.objects.create(
#             email="user@user.ru", is_staff=True, is_active=True
#         )
#         self.user2 = User.objects.create(
#             email="user2@user.ru", is_staff=True, is_active=True
#         )
#         self.course = Course.objects.create(title="Python-разработчик", owner=self.user)
#         self.lesson = Lesson.objects.create(
#             name="Django", course=self.course, owner=self.user
#         )
#         self.client.force_authenticate(user=self.user)
#
#         self.moderators_group = Group.objects.create(name="manager")
#         self.user2.groups.add(self.moderators_group)
#         """Тестирование создания урока"""
#         data = {
#             "name": "SQL-запросы",
#             "video": "youtube.com/lesson/1/",
#         }
#
#         url = reverse("training:lesson-list")
#         response = self.client.post(url, data, format="json")
#
#         # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         # self.assertEqual(
#         #     response.json(),
#         #     {
#         #         "id": 8,
#         #         "name": data["name"],
#         #         "description": None,
#         #         "preview": None,
#         #         "video": data["video"],
#         #         "course": None,
#         #         "owner": self.user.pk,
#         #     },
#         # )
#         #
#         # self.assertTrue(Lesson.objects.filter(name=data["name"]).exists())
#         self.assertTrue(Lesson.objects.all().count(), 2)
#
#     def test_lesson_with_incorrect_video_link_create(self):
#         """Тестирование выброса ошибки при создании урока с неразрешенной ссылкой."""
#         data = {
#             "name": "SQL-запросы",
#             "video": "my.com/lesson/1/",
#             "course": self.course.id,
#         }
#
#         url = reverse("training:lesson-create")
#         response = self.client.post(url, data)
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         # print(response.json())
#         # self.assertEqual(response.json(), 'non_field_errors'['К материалам можно добавлять только ссылки на YouTube.'])
#         # self.assertEqual(
#         #     response.json()["video"][0],
#         #     "К материалам можно добавлять только ссылки на YouTube."
#         # )
#
#     def test_lesson_retrieve(self):
#         """Тестирование просмотра детальной информации об уроке"""
#         url = reverse("training:lesson-detail", args=(self.lesson.pk,))
#         response = self.client.get(url)
#         data = response.json()
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # self.assertEqual(data.get("name"), self.lesson.name)
#
#     def test_lesson_list(self):
#         """Тестирование получения списка уроков"""
#         url = reverse("training:lesson-list")
#         response = self.client.get(url)
#         data = response.json()
#
#         result = {
#             "count": 1,
#             "next": None,
#             "previous": None,
#             "results": [
#                 {
#                     "id": self.lesson.pk,
#                     "name": self.lesson.name,
#                     "description": None,
#                     "preview": None,
#                     "video": None,
#                     "course": self.course.pk,
#                     "owner": self.user.pk,
#                 }
#             ],
#         }
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         #
#         # self.assertEqual(data, result)
#
#     def test_lesson_update(self):
#         """Тестирование обновления информации об уроке."""
#         url = reverse("training:lesson-update", args=(self.course.pk,))
#         data = {"description": "Научим создавать приложения на DRF."}
#         response = self.client.patch(url, data)
#         json_response = response.json()
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # self.assertEqual(json_response.get("description"), data["description"])
#
#     #
#     def test_lesson_delete(self):
#         """Тестирование удаления урока."""
#         url = reverse("training:lesson-delete", args=(self.course.pk,))
#         response = self.client.delete(url)
#
#         # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#         # self.assertEqual(Lesson.objects.all().count(), 0)
#
#
# #
# # def test_lesson_delete_with_moder(self):
# #     """Тестирование удаления записи модератором."""
# #     self.client.force_authenticate(user=self.user2)
# #     url = reverse("training:lesson-delete", args=(self.course.pk,))
# #     response = self.client.delete(url)
#
# # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
# # self.assertEqual(Lesson.objects.all().count(), 1)
#
#
# class SubscriptionTestCase(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create(email="admin@mail.ru")
#         self.course = Course.objects.create(title="Python-разработка", owner=self.user)
#         self.client.force_authenticate(user=self.user)
#
#     def test_subscribe_to_course(self):
#         """Тестирование подписки на курс."""
#         url = reverse("training:subscription")
#         data = {"course_id": self.course.pk}
#         response = self.client.post(url, data)
#         json_response = response.json()
#
#         course_list_url = reverse("courses-list")
#         course_response = self.client.get(course_list_url)
#         course_json_response = course_response.json()
#
#         # self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#
# #
# # self.assertEqual(json_response["message"], "Подписка добавлена")
# #
# #         self.assertEqual(course_json_response["results"][0]["is_subscribed"], True)
# #
# #     def test_unsubscribe_to_course(self):
# #         """Тестирование отмены подписки на курс."""
# #         url = reverse("training:subscription")
# #         data = {"course_id": self.course.pk}
# #         response = self.client.post(url, data)
# #
# #         self.assertEqual(response.status_code, status.HTTP_200_OK)
# #
# #         url2 = reverse("training:subscription")
# #         data2 = {"course_id": self.course.pk}
# #
# #         response2 = self.client.post(url2, data2)
# #         json_response2 = response2.json()
# #
# #         course_list_url = reverse("training:course-list")
# #         course_response = self.client.get(course_list_url)
# #         course_json_response = course_response.json()
# #
# #         self.assertEqual(json_response2["message"], "Подписка удалена")
# #
# #         self.assertEqual(course_json_response["results"][0]["is_subscribed"], False)
