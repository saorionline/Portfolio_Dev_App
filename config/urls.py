from django.urls import path

from portfolio.views import dashboard

urlpatterns = [
    path("", dashboard, name="dashboard"),
]
