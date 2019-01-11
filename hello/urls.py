from django.urls import path

from hello import views
from hello.models import LogMessage



urlpatterns = [
    path("", views.status, name="status"),
    path("last30d/", views.last30d, name="last30d"),
    path("last50t/", views.last50t, name="last50t"),
    path("about/", views.about, name="about"),
    path("detail/<barcode>", views.detail, name="detail"),
]
