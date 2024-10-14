from django.contrib import admin
from django.urls import path
from mainapp.views import (
    index,
    dummy_and_slow_view,
    ReportCreateView,
    ReportDetailView,
    ReportListView,
)

urlpatterns = [
    path("", index),
    path("dummy_and_slow_view", dummy_and_slow_view, name="dummy_and_slow_view"),
    path("report", ReportListView.as_view(), name="report_list"),
    path("report/create", ReportCreateView.as_view(), name="report_create"),
    path("report/detail/<int:pk>", ReportDetailView.as_view(), name="report_detail"),
    path("admin/", admin.site.urls),
]
