from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse
from .models import Report
from django.shortcuts import render
from .tasks import dummy_and_slow
import time


def index(request):
    return render(request, "mainapp/index.html")


def dummy_and_slow_view(request):  # new
    start_time = time.time()
    dummy_and_slow.delay()
    end_time = time.time()
    execution_time = end_time - start_time
    context = {
        "task_name": "Dummy and slow",
        "execution_time": round(execution_time, 2),
    }
    return render(request, "mainapp/generic.html", context=context)


class ReportCreateView(CreateView):
    model = Report
    fields = [
        "complexity",
    ]
    template_name = "mainapp/report_form.html"

    def get_success_url(self):
        return reverse("report_detail", kwargs={"pk": self.object.pk})


class ReportDetailView(DetailView):
    model = Report
    context_object_name = "report"
    template_name = "mainapp/report_detail.html"


class ReportListView(ListView):
    model = Report
    template_name = "mainapp/report_list.html"
    context_object_name = "reports"
    ordering = ["-dt_created"]
    paginate_by = 10
