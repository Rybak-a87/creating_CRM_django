from django.shortcuts import render
from django.views.generic import View, UpdateView, DeleteView, ListView
from django.http import HttpResponseRedirect

from .models import CompanyInformation, ProjectForCompany, Interaction
from .forms import CreateCompanyForm, CreateProjectForm, CreateInteractionForm


class MainListView(ListView):
    """
    Главная страница
    вывод всех компаний
    """
    model = CompanyInformation
    template_name = "mainapp/main_page.html"
    context_object_name = "companies"
    paginate_by = 3

    def get_ordering(self):
        ordering = self.request.GET.get("order_by")
        return ordering


class DetailCompanyView(View):
    """
    Вывод детальной информации о компании
    """
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        company = CompanyInformation.objects.get(id=id)
        projects = ProjectForCompany.objects.filter(company__name_company=company.name_company)
        context = {
            "company": company,
            "projects": projects
        }
        return render(request, "mainapp/company_detail.html", context)


class CreateCompanyView(View):
    """
    Добавить новую компанию в базу
    """
    def get(self, request, *args, **kwargs):
        form = CreateCompanyForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, "mainapp/company_create.html", context)

    def post(self, request, *args, **kwargs):
        form = CreateCompanyForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        else:
            context = {
                "form": form,
            }
            return render(request, "mainapp/company_create.html", context)


class CompanyUpdateView(UpdateView):
    """
    Изменение данных компании
    """
    model = CompanyInformation
    template_name = "mainapp/company_create.html"
    form_class = CreateCompanyForm


class CompanyDeleteView(DeleteView):
    """
    Удаление компании с базы
    """
    model = CompanyInformation
    template_name = "mainapp/company_delete.html"
    success_url = "/"


class ProjectsListView(ListView):
    """
    Страница вывода проектов
    """
    model = ProjectForCompany
    template_name = "mainapp/projects_in_work.html"
    context_object_name = "projects"
    # paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        projects_status = self.request.GET.get("projects_status")
        context = super().get_context_data(**kwargs)
        if projects_status:
            if projects_status == "in_work":
                projects_status = False
            elif projects_status == "finished":
                projects_status = True

            context["projects"] = self.model.objects.filter(finished=projects_status)
        return context


class DetailProjectView(View):
    """
    Вывод детальной информации о проекте
    """
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        project = ProjectForCompany.objects.get(id=id)
        interactions = Interaction.objects.filter(project__name_project=project.name_project)
        context = {
            "project": project,
            "interactions": interactions
        }
        return render(request, "mainapp/project_detail.html", context)


class CreateProjectView(View):
    """
    Добавить новый проект в базу
    """
    def get(self, request, *args, **kwargs):
        form = CreateProjectForm(request.POST or None)
        context = {
            "form": form
        }
        return render(request, "mainapp/project_create.html", context)

    def post(self, request, *args, **kwargs):
        form = CreateProjectForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/projects")
        else:
            context = {
                "form": form
            }
            return render(request, "mainapp/project_create.html", context)


class ProjectUpdateView(UpdateView):
    """
    Изменение данных проекта
    """
    model = ProjectForCompany
    template_name = "mainapp/project_create.html"
    form_class = CreateProjectForm


class ProjectDeleteView(DeleteView):
    """
    Удаление проекта с базы
    """
    model = ProjectForCompany
    template_name = "mainapp/company_delete.html"
    success_url = "/projects"


class InteractionListView(ListView):
    """
    Вывод взаимодействий с последующей фильтрацией
    """
    model = Interaction
    context_object_name = "interactions"
    template_name = "mainapp/interaction.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        company = self.request.GET.get("company")
        project = self.request.GET.get("project")
        if company:
            context["interactions"] = self.model.objects.filter(company__name_company=company)
        elif project:
            context["interactions"] = self.model.objects.filter(project__name_project=project)
        return context


class DetailInteractionView(View):
    """
    Вывод отдельного сообщения
    """
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        interaction = Interaction.objects.get(id=id)
        context = {
            "interaction": interaction
        }
        return render(request, "mainapp/interaction_detail.html", context)


class CreateInteractionView(View):
    """
    Добавление взаимодействия по проекту
    """
    def get(self, request, *args, **kwargs):
        project = ProjectForCompany.objects.get(id=kwargs.get("pk"))
        form = CreateInteractionForm(request.POST or None)
        context = {
            "form": form,
            "project": project
        }
        return render(request, "mainapp/interaction_create.html", context)

    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        project = ProjectForCompany.objects.get(id=id)
        print(project.name_project, project.company)
        form = CreateInteractionForm(request.POST or None)
        if form.is_valid():
            new_interaction = form.save(commit=False)
            new_interaction.project = ProjectForCompany.objects.get(name_project=project.name_project)
            new_interaction.company = CompanyInformation.objects.get(name_company=project.company)
            new_interaction.communication_channel = form.cleaned_data["communication_channel"]
            new_interaction.manager = form.cleaned_data["manager"]
            new_interaction.about = form.cleaned_data["about"]
            new_interaction.save()
            return HttpResponseRedirect(f"/project/{id}/")
        else:
            context = {
                "form": form,
                "project": project
            }
            return render(request, "mainapp/interaction_create.html", context)


class InteractionUpdateView(UpdateView):
    """
    Изменение данных проекта
    """
    model = Interaction
    template_name = "mainapp/interaction_create.html"
    form_class = CreateInteractionForm


class InteractionDeleteView(DeleteView):
    """
    Удаление проекта с базы
    """
    model = Interaction
    template_name = "mainapp/company_delete.html"
    success_url = "/interactions/"


class ManagerView(View):
    def get(self, request, *args, **kwargs):
        username = request.user.username
        print(username)
        interactions = Interaction.objects.filter(manager__username=username)
        context = {
            "interactions": interactions
        }
        return render(request, "mainapp/manager.html", context)
