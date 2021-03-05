from django.contrib import admin

from .models import CompanyInformation, ProjectForCompany, Interaction, SiteUser


admin.site.register(CompanyInformation)
admin.site.register(ProjectForCompany)
admin.site.register(SiteUser)


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    fields = (
        "project",
        "company",
        "communication_channel",
        "manager",
        "about"
    )
