from django import forms

# капча
from captcha.fields import CaptchaField

from .models import Account


class LoginForm(forms.ModelForm):
    """
    Форма для авторизации пользователя
    """
    # капча
    captcha = CaptchaField()

    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Логин",
        "style": "margin-top: 20px;"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Пароль",
        "style": "margin: 20px 0px;"
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["password"].label = ""
        self.fields["captcha"].label = ""

    def clean(self):
        """
        Проверка введенных username и password на соответствие для входа
        """
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        if not Account.objects.filter(username=username).exists():
            raise forms.ValidationError(f"Пользователь {username} не найден")
        user = Account.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Не верный пароль")
        return self.cleaned_data

    class Meta:
        model = Account
        fields = ["username", "password"]


class RegistrationForm(forms.ModelForm):
    """
    Форма регистрации пользователя
    """
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Логин",
        "style": "margin-top: 20px;"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Пароль",
        "style": "margin-top: 20px;"
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Подтвердите пароль",
        "style": "margin-top: 20px;"
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Ваше имя",
        "style": "margin-top: 20px;"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Ваша фамилия",
        "style": "margin-top: 20px;"
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Электронная почта",
        "style": "margin-top: 20px; margin-bottom: 20px;"
    }))
    # TODO почему при активности, поле становится обязательным к заполнению (разобраться)
    # manager_status = forms.BooleanField(widget=forms.CheckboxInput(attrs={
    #     # "class": "btn-check",
    #     "id": "manager",
    # }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = ""
        self.fields["password"].label = ""
        self.fields["confirm_password"].label = ""
        self.fields["first_name"].label = ""
        self.fields["last_name"].label = ""
        self.fields["email"].label = ""
        self.fields["manager_status"].label = "Менеджер"

    def clean_username(self):
        """
        Проверка введенного username на совпадение в БД
        """
        username = self.cleaned_data["username"]
        if Account.objects.filter(username=username).exists():
            raise forms.ValidationError(f"Логин {username} уже зарегистрирован")
        return username

    def clean_email(self):
        """
        Проверка введенного email на совпадение в БД
        """
        email = self.cleaned_data["email"]
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError(f"{email} уже зарегистрирован")
        return email

    def clean(self):
        """
        Проверка введенных паролей на совпадение
        """
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return self.cleaned_data

    class Meta:
        model = Account
        fields = [
            "username",
            "password",
            "confirm_password",
            "first_name",
            "last_name",
            "email",
            "manager_status"
        ]


class UpdateUserForm(forms.ModelForm):
    """
    Форма изменения имени, фамилии и почты пользователя
    """
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "style": "margin-top: 20px;"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "style": "margin-top: 20px; margin-bottom: 30px;",
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "style": "margin-top: 20px; margin-bottom: 20px;"
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].label = "Имя"
        self.fields["last_name"].label = "Фамилия"
        self.fields["email"].label = "Электронная почта"

    def clean_email(self):
        """
        Проверка введенного email на совпадение в БД
        """
        email = self.cleaned_data["email"]
        # TODO доработать проверку email при его редактировании
        if Account.objects.filter(email=email).count() > 1:
            raise forms.ValidationError(f"{email} уже зарегистрирован")
        return email

    class Meta:
        model = Account
        fields = [
            "first_name",
            "last_name",
            "email",
        ]


class UpdatePassForm(forms.ModelForm):
    """
    Форма обновление пароля
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Новый пароль",
        "style": "margin-top: 30px;"
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Подтвердите новый пароль",
        "style": "margin-top: 20px;"
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].label = ""
        self.fields["confirm_password"].label = ""

    def clean(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают")
        return self.cleaned_data

    class Meta:
        model = Account
        fields = [
            "password",
            "confirm_password",
        ]


class UpdatePhotoForm(forms.ModelForm):
    """
    Форма добавление фото к профилю
    """
    # TODO разобраться и доделать добавление фото к профилю
    # photo = forms.ImageField(widget=forms.FileInput())
    class Meta:
        model = Account
        fields = ["photo"]
