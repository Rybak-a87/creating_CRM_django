from django import forms

from .models import CompanyInformation, ProjectForCompany


class CreateCompanyForm(forms.ModelForm):
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
            "about_company": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Краткое описание",
                "minlength": "20"
            }),
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


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectForCompany
        fields = "__all__"

        widgets = {
            "company": forms.Select(attrs={
                "class": "form-control",
                "placeholder": "Компания"
            }),
            "name_project": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Название проекта"
            }),
            "about_project": forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Краткое описание",
                "minlength": "20"
            }),
            "start_date": forms.SelectDateWidget(attrs={}),
            "finish_date": forms.SelectDateWidget(attrs={}),
            "price": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Стоимость"
            })
        }