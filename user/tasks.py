from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from user.models import User


@shared_task
def deactivate_inactive_users():
    """Блокировка пользователей, которые не заходили более месяца"""
    month_ago = timezone.now() - timedelta(months=1)
    count = 0

    filter_login = {"last_login__lte": month_ago, "is_active": True}
    inactive_users = User.objects.filter(**filter_login)

    count = inactive_users.update(is_active=False)

    return f"Заблокировано {count} неактивных пользователей"
