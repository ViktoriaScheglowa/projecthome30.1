from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название')
    preview = models.ImageField(
        upload_to="media/preview",
        verbose_name="Изображение",
        blank=True,
        null=True,
        help_text="Загрузите изображение курса", )
    description = models.TextField(
        blank=True,
        verbose_name='Описание')
    owner = models.ForeignKey("user.User",
                              on_delete=models.SET_NULL,
                              null=True,
                              blank=True,
                              verbose_name="Создатель курса",
                              )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления курса'
    )
    notification_task_id = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name='id задачи уведомления'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'
        ordering = ['title']


class Lesson(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name='Название')
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание')
    preview = models.ImageField(
        upload_to='media/photos',
        blank=True,
        null=True,
        verbose_name='Изображение')
    video = models.CharField(
        max_length=250,
        verbose_name="Ссылка на видео",
        help_text="Вставьте ссылку на видео",
        null=True,
        blank=True, )
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='lessons')
    owner = models.ForeignKey("user.User",
                              verbose_name='Владелец',
                              help_text='Укажите владельца',
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL)
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления урока'
    )

    def __str__(self):
        return f"Курс: {self.course}" f"Урок: {self.name}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, verbose_name="Пользователь подписки"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Подписка на курс"
    )

    def __str__(self):
        return f"{self.user.email} подписан(а) на {self.course.title}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
