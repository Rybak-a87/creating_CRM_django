from django.db import models
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class CompanyInformation(models.Model):
    name_company = models.CharField(verbose_name="Название компании", max_length=255)
    contact_person = models.CharField(verbose_name="Контактное лицо", max_length=255)
    # about_company = RichTextUploadingField(verbose_name="Краткое описание")
    about_company = models.TextField(verbose_name="Краткое описание")
    create_date = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    date_of_change = models.DateTimeField(verbose_name="Дата последнего изменения", auto_now=True)
    address = models.CharField(verbose_name="Адрес", max_length=255)
    phone = models.CharField(verbose_name="Номер телефона", max_length=255)
    email = models.EmailField(verbose_name="E-mail")

    def get_absolute_url(self):
        return f"/company/{self.id}"

    def __str__(self):
        return self.name_company

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Информация о клиентах"


class ProjectForCompany(models.Model):
    company = models.ForeignKey(CompanyInformation, verbose_name="Компания", on_delete=models.CASCADE)
    name_project = models.CharField(verbose_name="Название проекта", max_length=255)
    about_project = models.TextField(verbose_name="Описание")
    start_date = models.DateField(verbose_name="Срок начала")
    finish_date = models.DateField(verbose_name="Срок окончания", null=True, blank=True)
    price = models.FloatField(verbose_name="Стоимость")

    def get_absolute_url(self):
        return f"/project/{self.id}"

    def __str__(self):
        return self.name_project

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты для компаний"


class Interaction(models.Model):
    CHANNEL_CHOICES = (
        ("application", "Заявка"),
        ("mail", "Письмо"),
        ("site", "Сайт"),
        ("initiative", "Инициатива компании")
    )
    project = models.ForeignKey(ProjectForCompany, verbose_name="Проект", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyInformation, verbose_name="Компания", on_delete=models.CASCADE)
    communication_channel = models.CharField(
        verbose_name="Канал общения",
        max_length=30,
        choices=CHANNEL_CHOICES
    )
    manager = models.ForeignKey(User, verbose_name="Менеджер", on_delete=models.CASCADE)
    about = models.TextField(verbose_name="Описание")
    rating = models.IntegerField(verbose_name="Оценка", default=0)

    def __str__(self):
        return f"{self.project} ] {self.manager}"

    class Meta:
        verbose_name = "Взаимодействие"
        verbose_name_plural = "Взаимодействия"


class SiteUser(models.Model):
    photo = models.ImageField(verbose_name="Фото", upload_to="user_photo/", null=True, blank=True)
    first_name = models.CharField(verbose_name="Имя", max_length=255)
    last_name = models.CharField(verbose_name="Фамилия", max_length=255)
    email = models.EmailField(verbose_name="Электронная почта")
    password = models.CharField(verbose_name="Пароль", max_length=255)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        verbose_name = "Пользователь сайта"
        verbose_name_plural = "Пользователи сайта"

