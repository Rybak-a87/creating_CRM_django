from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import CompanyInformation, ProjectForCompany, Interaction, RatingInteraction


class CompanyInformationAdminForm(forms.ModelForm):
    """
    Форма для отображения CKEditor в админке
    """
    about_company = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = CompanyInformation
        fields = "__all__"


@admin.register(CompanyInformation)
class CompanyInformationAdmin(admin.ModelAdmin):
    form = CompanyInformationAdminForm
    fields = (
        "name_company",
        "contact_person",
        "about_company",
        "address",
        "phone",
        "email"
    )


admin.site.register(ProjectForCompany)
admin.site.register(RatingInteraction)


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    fields = (
        "project",
        "company",
        "communication_channel",
        "manager",
        "about"
    )
