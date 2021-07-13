from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# class Account(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     photo = models.ImageField(verbose_name="Фото пользователя", upload_to="user_photo/", null=True, blank=True)
#     manager_status = models.BooleanField(verbose_name="Вы менеджер?", default=False)


class Account(AbstractUser):
    """
    Добавление к модели User дополнительных полей
    """
    # ! дополнительно в setting.py необходимо добавить:
    # ! AUTH_USER_MODEL = "account.Account" (AUTH_USER_MODEL = "app_name.class_name")
    email = models.EmailField(unique=True)
    photo = models.ImageField(verbose_name="Фото пользователя", upload_to="user_photo/", null=True, blank=True)
    manager_status = models.BooleanField(verbose_name="Менеджер", default=False)

    # для регистрации при помощи email
    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    def get_absolute_url(self):
        return "/user"
