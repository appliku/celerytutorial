from django.contrib import admin
from django.urls import path
from mainapp.views import index

urlpatterns = [
    path("", index),
    path("admin/", admin.site.urls),
]
