from django.shortcuts import render
from django.views.generic import View, UpdateView, DeleteView, ListView
from django.http import HttpResponseRedirect

from .models import CompanyInformation, ProjectForCompany
from .forms import CreateCompanyForm, CreateProjectForm


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
        ordering = self.request.GET.get("order_by", "name_company")
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
    template_name = "mainapp/projects_in_work.html"
    context_object_name = "projects"
    paginate_by = 3

    def get_queryset(self):
        queryset = ProjectForCompany.objects.all()
        return queryset


class DetailProjectView(View):
    """
    Вывод детальной информации о проекте
    """
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        project = ProjectForCompany.objects.get(id=id)
        context = {
            "project": project
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
