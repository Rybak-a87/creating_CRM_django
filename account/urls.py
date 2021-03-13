from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


app_name = "account"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("registration/", views.RegistrationView.as_view(), name="registration"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("update/<int:pk>/", views.AccountUpdateView.as_view(), name="update_user"),
    path("update/pass<int:pk>/", views.PassUpdateView.as_view(), name="update_pass"),
    path("update/photo<int:pk>/", views.PhotoUpdateView.as_view(), name="update_photo"),
]

