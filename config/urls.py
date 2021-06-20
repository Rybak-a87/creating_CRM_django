from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("mainapp.urls")),
    path("account/", include("account.urls")),
    # ckeditor
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # капча
    path("captcha/", include("captcha.urls")),
]

if settings.DEBUG:
    # Django debug toolbar
    # import debug_toolbar
    # urlpatterns = [
    #     path("__debug__/", include(debug_toolbar.urls)),
    # ] + urlpatterns

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
