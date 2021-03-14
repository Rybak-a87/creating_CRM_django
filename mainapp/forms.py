from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import CompanyInformation, ProjectForCompany, Interaction


class CreateCompanyForm(forms.ModelForm):
    """
    Форма для добавления и редактирования компании (клиента)
    """
    class Meta:
        model = CompanyInformation
        fields = "__all__"

        widgets = {
            "name_company": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Компания"
            }),
            "contact_person": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Контактное лицо"
            }),
            "about_company": CKEditorUploadingWidget(),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Адрес"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Номер телефона"
            }),
            "email": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Электронная почта"
            })
        }


class CreateProjectWithCompanyForm(forms.ModelForm):
    """
    Форма для добавления проекта со страницы с описанием компании
    """
    class Meta:
        model = ProjectForCompany
        fields = (
            "name_project",
            "about_project",
            "start_date",
            "finished",
            "finish_date",
            "price"
        )

        widgets = {
            "name_project": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Название проекта"
            }),
            "about_project": CKEditorUploadingWidget(),
            "start_date": forms.SelectDateWidget(attrs={}),
            "finish_date": forms.SelectDateWidget(attrs={}),
            "price": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Стоимость"
            })
        }


class CreateProjectForm(CreateProjectWithCompanyForm):
    """
    Форма для добавления проекта
    """
    CreateProjectWithCompanyForm.Meta.fields = "__all__"
    CreateProjectWithCompanyForm.Meta.widgets |= {
        "company": forms.Select(attrs={
            "class": "form-control",
            "placeholder": "Компания"
        })
    }


class CreateInteractionWithProjectForm(forms.ModelForm):
    """
    Форма для добавления и редактирования зависимости со страницы описания проекта
    """
    class Meta:
        model = Interaction
        fields = ["communication_channel", "about"]

        widgets = {
            "about": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Описание"
            }),
            "communication_channel": forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Канал общения"
            })

        }


class CreateInteractionForm(CreateInteractionWithProjectForm):
    """
    Форма для добавления зависимости
    """
    CreateInteractionWithProjectForm.Meta.fields += [
        "project",
    ]
    CreateInteractionWithProjectForm.Meta.widgets |= {
        "project": forms.Select(attrs={
            "class": "form-control",
            "placeholder": "Канал общения"
        })
    }
