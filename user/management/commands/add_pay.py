from django.core.management import BaseCommand

from training.models import Course
from user.models import Pay, User


class Command(BaseCommand):
    help = "Adding payment to the database"

    def handle(self, *args, **kwargs):
        user1, _ = User.objects.get_or_create(email="user@user.com")
        user2, _ = User.objects.get_or_create(email="user1@user.com")
        user3, _ = User.objects.get_or_create(email="user2@user.com")

        course1, _ = Course.objects.get_or_create(id=1)
        course2, _ = Course.objects.get_or_create(id=2)

        pays = [
            {
                "user": user1,
                "payment_date": "2025-08-02",
                "course": course1,
                "lesson": None,
                "amount": 15000,
                "form_of_payment": Pay.TRANSFER,
            },
            {
                "user": user2,
                "payment_date": "2025-07-28",
                "course": course1,
                "lesson": None,
                "amount": 25000,
                "form_of_payment": Pay.TRANSFER,
            },
            {
                "user": user3,
                "payment_date": "2025-06-28",
                "course": course2,
                "lesson": None,
                "amount": 13000,
                "form_of_payment": Pay.CASH,
            },
        ]

        for pay in pays:
            payment, created = Pay.objects.get_or_create(**pay)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Информация по оплате добавлена: "
                        f"{payment.user.email} - {payment.course.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Информация уже была добавлена ранее: "
                        f"{payment.user.email} - {payment.course.name}"
                    )
                )
