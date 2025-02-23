from django.urls import path
from . import views

urlpatterns = [
    path("receive-schedule/", views.receive_schedule, name="receive_schedule"),
    path(
        "get-schedule-history/", views.get_schedule_history, name="get_schedule_history"
    ),
]
