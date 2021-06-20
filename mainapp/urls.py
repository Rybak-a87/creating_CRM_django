from django.urls import path

# кэширование
from django.views.decorators.cache import cache_page

from . import views


time_cache = 60    # время хранения кеша 60 секунд
app_name = "mainapp"

urlpatterns = [
    # companies page (main)
    path("", views.MainListView.as_view(), name="main_page"),
    path("company/<int:pk>/", cache_page(time_cache)(views.DetailCompanyView.as_view()), name="detail_company"),
    path("company/create_new/", views.CreateCompanyView.as_view(), name="create_company"),
    path("company/<int:pk>/update/", views.CompanyUpdateView.as_view(), name="update_company"),
    path("company/<int:pk>/delete/", views.CompanyDeleteView.as_view(), name="delete_company"),
    # projects page
    path("projects/", cache_page(time_cache)(views.ProjectsListView.as_view()), name="projects_page"),
    path("project/<int:pk>/", cache_page(time_cache)(views.DetailProjectView.as_view()), name="detail_project"),
    path("project/create_new/", views.CreateProjectView.as_view(), name="create_project"),
    path("project/<int:pk>/update/", views.ProjectUpdateView.as_view(), name="update_project"),
    path("project/<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="delete_project"),
    # interaction
    path("interactions/", cache_page(time_cache)(views.InteractionListView.as_view()), name="interaction_page"),
    path("interaction/<int:pk>/", cache_page(time_cache)(views.DetailInteractionView.as_view()), name="interaction_detail"),
    path("interaction/create/", views.CreateInteractionView.as_view(), name="create_interaction"),
    path("interaction/<int:pk>/update/", views.InteractionUpdateView.as_view(), name="update_interaction"),
    path("interaction/<int:pk>/delete", views.InteractionDeleteView.as_view(), name="delete_interaction"),
    # manager
    path("user/", views.ManagerView.as_view(), name="manager"),
    # likes
    path("add_like/", views.AddLikeView.as_view(), name="like_add"),
    path("remove_like/", views.RemoveLikeView.as_view(), name="like_remove"),
]
