# urls.py principal
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("tareas/", include('tareas.urls', namespace='tareas')),  # línea para incluir las URLs de 'tareas'
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
