from django.shortcuts import render
from django.views.generic import View, UpdateView, DeleteView, ListView, DetailView
from django.http import HttpResponseRedirect

from .filters import InteractionFilter

from .models import CompanyInformation, ProjectForCompany, Interaction, RatingInteraction
from .forms import (
    CreateCompanyForm,
    CreateProjectForm,
    CreateInteractionWithProjectForm,
    CreateProjectWithCompanyForm,
    CreateInteractionForm
)
from django.contrib.auth import get_user_model

User = get_user_model()


class MainListView(ListView):
    """
    Главная страница
    вывод всех компаний с пагинацией и сортировкой
    """
    model = CompanyInformation
    template_name = "mainapp/main_page.html"
    context_object_name = "companies"
    paginate_by = 3

    def get_ordering(self):
        ordering = self.request.GET.get("order_by")
        return ordering

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order_by"] = self.request.GET.get("order_by")
        return context


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


# # TODO переписать класс DetailCompanyView с View на DetailView (переделать get_absolute_url и применить его везде)
# class CompanyDetailView(DetailView):
#     """
#     Вывод детальной информации о компании с перечнем списка проектов компании
#     """
#     model = CompanyInformation
#     pk_url_kwarg = "pk"
#     template_name = "mainapp/company_detail.html"
#     context_object_name = "company"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context


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
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        projects_status = self.request.GET.get("order_by")
        if projects_status:
            context["order_by"] = projects_status
    #         if projects_status == "in_work":
    #             projects_status = False
    #         elif projects_status == "finished":
    #             projects_status = True
    #
    #         context["projects"] = self.model.objects.filter(finished=projects_status)
    #
        return context

    def get_queryset(self):
        projects_status = self.request.GET.get("order_by")
        if projects_status:
            if projects_status == "in_work":
                projects_status = False
            elif projects_status == "finished":
                projects_status = True

            return ProjectForCompany.objects.filter(finished=projects_status)

        return ProjectForCompany.objects.all()


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
    обработкой гет запроса
    """
    def get(self, request, *args, **kwargs):
        company_id = request.GET.get("company_id")
        if company_id:
            form = CreateProjectWithCompanyForm(request.POST or None)
        else:
            form = CreateProjectForm(request.POST or None)

        context = {
            "form": form
        }
        return render(request, "mainapp/project_create.html", context)

    def post(self, request, *args, **kwargs):
        company_id = request.GET.get("company_id")
        if company_id:
            form = CreateProjectWithCompanyForm(request.POST or None)
        else:
            form = CreateProjectForm(request.POST or None)

        if form.is_valid():
            if company_id:
                new_project = form.save(commit=False)
                new_project.company = CompanyInformation.objects.get(id=company_id)
                new_project.save()
                return HttpResponseRedirect("/projects")
            else:
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
    form_class = CreateProjectWithCompanyForm


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
        context["filter"] = InteractionFilter(self.request.GET, queryset=self.get_queryset())

        # ! Кастомный фильтр
        # TODO доделать корректную работу фильтра и поиск по ключевым словам
        # context["companies_list"] = tuple(set([i.company.name_company for i in self.model.objects.all()]))
        # context["projects_list"] = tuple(set([i.project.name_project for i in self.model.objects.all()]))
        # company = self.request.GET.get("company")
        # project = self.request.GET.get("project")
        # if company:
        #     context["interactions"] = self.model.objects.filter(company__name_company=company)
        # elif project:
        #     context["interactions"] = self.model.objects.filter(project__name_project=project)

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
    с обработкой гет запроса
    """
    def get(self, request, *args, **kwargs):
        project_id = request.GET.get("project_id")
        if project_id:
            project = ProjectForCompany.objects.get(id=project_id)
            form = CreateInteractionWithProjectForm(request.POST or None)
            context = {
                "form": form,
                "project": project
            }
            return render(request, "mainapp/interaction_create_with_project.html", context)
        else:
            form = CreateInteractionForm(request.POST or None)
            context = {
                "form": form,
            }
            return render(request, "mainapp/interaction_create.html", context)

    def post(self, request, *args, **kwargs):
        project_id = request.GET.get("project_id")
        if project_id:
            project = ProjectForCompany.objects.get(id=project_id)
            form = CreateInteractionWithProjectForm(request.POST or None)
            if form.is_valid():
                new_interaction = form.save(commit=False)
                new_interaction.project = ProjectForCompany.objects.get(name_project=project.name_project)
                new_interaction.company = CompanyInformation.objects.get(name_company=project.company)
                new_interaction.manager = User.objects.get(username=self.request.user.username)
                new_interaction.save()
                return HttpResponseRedirect(f"/project/{project_id}/")
            else:
                context = {
                    "form": form,
                    "project": project
                }
                return render(request, "mainapp/interaction_create_with_project.html", context)
        else:
            form = CreateInteractionForm(request.POST or None)
            if form.is_valid():
                new_interaction = form.save(commit=False)
                project = ProjectForCompany.objects.get(name_project=form.cleaned_data["project"])
                new_interaction.company = CompanyInformation.objects.get(name_company=project.company.name_company)
                new_interaction.manager = User.objects.get(username=self.request.user.username)
                new_interaction.save()
                return HttpResponseRedirect(f"/interactions/")
            else:
                context = {
                    "form": form,
                }
                return render(request, "mainapp/interaction_create.html", context)


class InteractionUpdateView(UpdateView):
    """
    Изменение данных проекта
    """
    model = Interaction
    template_name = "mainapp/interaction_create_with_project.html"
    form_class = CreateInteractionWithProjectForm


class InteractionDeleteView(DeleteView):
    """
    Удаление проекта с базы
    """
    model = Interaction
    template_name = "mainapp/company_delete.html"
    success_url = "/interactions/"


class ManagerView(View):
    """
    Кабинет менеджера (страничка пользователя)
    """
    def get(self, request, *args, **kwargs):
        username = request.user.username
        interactions = Interaction.objects.filter(manager__username=username)
        context = {
            "interactions": interactions
        }
        return render(request, "mainapp/manager.html", context)


class AddLikeView(View):
    """
    Добавление лайка к взаимодействию
    """
    def post(self, request, *args, **kwargs):
        interaction_id = int(request.POST.get("interaction_id"))
        user_id = int(request.POST.get("user_id"))
        url_from = request.POST.get("url_from")

        interaction = Interaction.objects.get(id=interaction_id)
        user = User.objects.get(id=user_id)

        try:
            interaction_like_inst = RatingInteraction.objects.get(
                interaction=interaction,
                manager=user
            )
        except Exception as ex:
            interaction_like = RatingInteraction(
                interaction=interaction,
                manager=user,
                like=True
            )
            interaction_like.save()
        return HttpResponseRedirect(url_from)


class RemoveLikeView(View):
    """
    Удаление лайк с БД
    """
    def post(self, request, *args, **kwargs):
        interaction_likes_id = int(request.POST.get("interaction_likes_id"))
        url_from = request.POST.get("url_from")

        interaction_like = RatingInteraction.objects.get(id=interaction_likes_id)
        interaction_like.delete()
        return HttpResponseRedirect(url_from)
