from django.shortcuts import render
from django.views.generic import View, UpdateView
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect

from .models import Account
from .forms import LoginForm, RegistrationForm, UpdateUserForm, UpdatePassForm, UpdatePhotoForm


class LoginView(View):
    """
    Авторизация пользователя
    """
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            "form": form,
            "title": "Авторизация"
        }
        return render(request, "account/login.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect("/")
        context = {
            "form": form,
            "title": "Авторизация"
        }
        return render(request, "account/login.html", context)


class RegistrationView(View):
    """
    Регистрация пользователя
    """
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            "form": form,
            "title": "Регистрация"
        }
        return render(request, "account/login.html", context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data["username"]
            new_user.first_name = form.cleaned_data["first_name"]
            new_user.last_name = form.cleaned_data["last_name"]
            new_user.email = form.cleaned_data["email"]
            new_user.manager_status = form.cleaned_data["manager_status"]
            new_user.save()
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            user = authenticate(username=new_user.username, password=form.cleaned_data["password"])
            if user:
                login(request, user)
                return HttpResponseRedirect("/")

        context = {
            "form": form,
            "title": "Регистрация"
        }
        return render(request, "account/login.html", context)


class AccountUpdateView(UpdateView):
    """
    Редактирование данных пользователя
    """
    model = Account
    template_name = "account/update_user.html"
    form_class = UpdateUserForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["check_user"] = self.kwargs.get("pk")
        context["title"] = "Редактирование данных"
        return context


class PassUpdateView(View):
    """
    Изменить пароль пользователя
    """
    def get(self, request, *args, **kwargs):
        form = UpdatePassForm(request.POST or None)
        check_user = kwargs.get("pk")
        context = {
            "form": form,
            "check_user": check_user,
            "title": "Смена пароля"
        }
        return render(request, "account/update_user.html", context)

    def post(self, request, *args, **kwargs):
        form = UpdatePassForm(request.POST or None)
        check_user = kwargs.get("pk")
        if form.is_valid():

            request.user.set_password(form.cleaned_data["password"])
            request.user.save()
            user = authenticate(username=request.user.username, password=form.cleaned_data["password"])
            if user:
                login(request, user)
                return HttpResponseRedirect("/user")

        context = {
            "form": form,
            "check_user": check_user,
            "title": "Смена пароля"
        }
        return render(request, "account/update_user.html", context)


class PhotoUpdateView(UpdateView):
    """
    Редактирование данных пользователя
    """
    model = Account
    template_name = "account/update_user.html"
    form_class = UpdatePhotoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["check_user"] = self.kwargs.get("pk")
        context["title"] = "Выбрать фото"
        return context


# TODO разобраться и доделать добавление фото к профилю через форму (class PhotoUpdateView)
# class PhotoUpdateView(View):
#     """
#     Изменить пароль пользователя
#     """
#     def get(self, request, *args, **kwargs):
#         form = UpdatePhotoForm(request.POST or None)
#         check_user = kwargs.get("pk")
#         context = {
#             "form": form,
#             "check_user": check_user,
#             "title": "Выбрать фото"
#         }
#         return render(request, "account/update_user.html", context)
#
#     def post(self, request, *args, **kwargs):
#         form = UpdatePhotoForm(request.POST, request.FILES)
#         check_user = kwargs.get("pk")
#         if form.is_valid():
#             a = request.FILES["photo"]
#             print(form.cl)
#             print(a)
#
#         context = {
#             "form": form,
#             "check_user": check_user,
#             "title": "Выбрать фото"
#         }
#         return render(request, "account/update_user.html", context)