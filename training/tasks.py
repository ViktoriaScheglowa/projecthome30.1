from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from training.models import Course, Subscription


@shared_task
def send_email(course_id=None):
    """Рассылка писем пользователям об обновлении материалов курса."""
    course = Course.objects.get(id=course_id)
    if timezone.now() - course.update_at >= timedelta(hours=4):
        subscriptions = Subscription.objects.filter(course=course)
        if subscriptions.exists():
            emails = [subscription.user.email for subscription in subscriptions]
            try:
                send_mail(
                    subject=f'Курс "{course.title}" обновлен',
                    message=f'Добрый день! Вы подписаны на обновление курса "{course.title}". Вы уже можете посмотреть '
                    f"их содержание с учетом изменений в личном кабинете.",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=emails,
                )
                print(f"Письма отправлены {len(emails)} подписчикам")
                return f"Уведомления отправлены для курса: {course.title}"
            except Exception as e:
                print(f"Ошибка при отправке письма: {str(e)}")
                send_email.retry(args=[course_id], exc=e, countdown=3600)

        return f"Нет подписчиков на курс: {course.title}"

    course.notification_task_id = None
    course.save()
