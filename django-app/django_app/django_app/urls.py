from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home(request):
    return HttpResponse("Django Monitoring OK")


urlpatterns = [
    path("admin/", admin.site.urls),

    # homepage
    path("home/", home),

    # prometheus endpoint
    path("", include("django_prometheus.urls")),
]