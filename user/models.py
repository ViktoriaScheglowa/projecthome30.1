from django.contrib.auth.models import AbstractUser
from django.db import models

from training.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name='email',
        help_text='Введите Ваш email'
    )
    avatar = models.ImageField(
        upload_to='media/avatars',
        verbose_name='Аватар',
        help_text='Загрузите изображение',
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        max_length=35,
        verbose_name='Номер телефона',
        help_text='Введите номер телефона',
        null=True,
        blank=True
    )
    country = models.CharField(
        max_length=50,
        verbose_name='Страна',
        help_text='Введите страну проживания',
    )
    token = models.CharField(
        max_length=50,
        verbose_name='Токен',
        null=True,
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return 'media/default_avatar.png'


class Pay(models.Model):
    CASH = 'Наличные'
    TRANSFER = 'Перевод на счет'

    PAYMENT_IN_CHOICES = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='user',
        verbose_name='Пользователь',
        null=True,
        blank=True
    )
    payment_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата оплаты'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name='Оплаченный курс',
        null=True,
        blank=True
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name='Оплаченный урок',
        null=True,
        blank=True
    )
    amount = models.PositiveIntegerField(
        verbose_name='Сумма оплаты',
        help_text='Введите сумму оплаты'
    )
    form_of_payment = models.CharField(
        max_length=15,
        choices=PAYMENT_IN_CHOICES,
        verbose_name='Способ оплаты',
        help_text='Выберите способ оплаты'
    )
