# Generated by Django 3.1.7 on 2021-03-12 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_company', models.CharField(max_length=255, verbose_name='Название компании')),
                ('contact_person', models.CharField(max_length=255, verbose_name='Контактное лицо')),
                ('about_company', models.TextField(verbose_name='Краткое описание')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_of_change', models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('phone', models.CharField(max_length=255, verbose_name='Номер телефона')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Информация о клиентах',
            },
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('communication_channel', models.CharField(choices=[('Заявка', 'Заявка'), ('Письмо', 'Письмо'), ('Сайт', 'Сайт'), ('Инициатива компании', 'Инициатива компании')], max_length=30, verbose_name='Канал общения')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания взаимодействия')),
                ('about', models.TextField(verbose_name='Описание')),
                ('like', models.PositiveIntegerField(default=0, verbose_name='Лайк')),
                ('dislike', models.PositiveIntegerField(default=0, verbose_name='Дизлайк')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.companyinformation', verbose_name='Компания')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Менеджер')),
            ],
            options={
                'verbose_name': 'Взаимодействие',
                'verbose_name_plural': 'Взаимодействия',
            },
        ),
        migrations.CreateModel(
            name='RatingInteraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='Лайк')),
                ('dislike', models.BooleanField(default=False, verbose_name='Дизлайк')),
                ('interaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.interaction', verbose_name='Взаимодействие')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Менеджер')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
            },
        ),
        migrations.CreateModel(
            name='ProjectForCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_project', models.CharField(max_length=255, verbose_name='Название проекта')),
                ('about_project', models.TextField(verbose_name='Описание')),
                ('start_date', models.DateField(verbose_name='Срок начала')),
                ('finished', models.BooleanField(default=False, verbose_name='Законченный проект')),
                ('finish_date', models.DateField(blank=True, null=True, verbose_name='Срок окончания')),
                ('price', models.FloatField(verbose_name='Стоимость')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.companyinformation', verbose_name='Компания')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты для компаний',
            },
        ),
        migrations.AddField(
            model_name='interaction',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.projectforcompany', verbose_name='Проект'),
        ),
    ]
