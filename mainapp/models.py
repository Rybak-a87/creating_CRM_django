from django.db import models
from django.contrib.auth import get_user_model
# from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class CompanyInformation(models.Model):
    """
    Модель компании (клиента)
    """
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
    """
    Модель проекта компании (клиента)
    """
    company = models.ForeignKey(CompanyInformation, verbose_name="Компания", on_delete=models.CASCADE)
    name_project = models.CharField(verbose_name="Название проекта", max_length=255)
    about_project = models.TextField(verbose_name="Описание")
    start_date = models.DateField(verbose_name="Срок начала")
    finished = models.BooleanField(verbose_name="Законченный проект", default=False)
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
    """
    Модель взаимодействия менеджера с клиентом по проекту
    """
    APPLICATION = ("Заявка", "Заявка")
    MAIL = ("Письмо", "Письмо")
    SITE = ("Сайт", "Сайт")
    INITIATIVE = ("Инициатива компании", "Инициатива компании")
    CHANNEL_CHOICES = (
        APPLICATION,
        MAIL,
        SITE,
        INITIATIVE
    )

    project = models.ForeignKey(ProjectForCompany, verbose_name="Проект", on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyInformation, verbose_name="Компания", on_delete=models.CASCADE)
    communication_channel = models.CharField(
        verbose_name="Канал общения",
        max_length=30,
        choices=CHANNEL_CHOICES
    )
    manager = models.ForeignKey(User, verbose_name="Менеджер", on_delete=models.CASCADE)
    date_create = models.DateTimeField(verbose_name="Дата создания взаимодействия", auto_now_add=True)
    about = models.TextField(verbose_name="Описание")
    like = models.PositiveIntegerField(verbose_name="Лайк", default=0)
    dislike = models.PositiveIntegerField(verbose_name="Дизлайк", default=0)

    def __str__(self):
        return f"{self.project} | {self.manager}"

    def get_absolute_url(self):
        return f"/interaction/{self.id}"

    class Meta:
        verbose_name = "Взаимодействие"
        verbose_name_plural = "Взаимодействия"


# TODO доделать систему рейтингов взаимодействий
class RatingInteraction(models.Model):
    """
    Модель рейтинг взаимодействия менеджера с клиентом
    """
    interaction = models.ForeignKey(Interaction, verbose_name="Взаимодействие", on_delete=models.CASCADE)
    manager = models.ForeignKey(User, verbose_name="Менеджер", on_delete=models.CASCADE)
    like = models.BooleanField(verbose_name="Лайк", default=False)
    dislike = models.BooleanField(verbose_name="Дизлайк", default=False)
    created_date = models.DateTimeField(verbose_name="Дата установки лайка", auto_now=True)

    def __str__(self):
        return f"{self.interaction.date_create} | {self.interaction.manager} | {'+' if self.like else '-'}"

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
