from django.contrib import admin
from django.urls import path
from mainapp.views import index, dummy_and_slow_view

urlpatterns = [
    path("", index),
    path("dummy_and_slow_view", dummy_and_slow_view, name="dummy_and_slow_view"),
    path("admin/", admin.site.urls),
]
