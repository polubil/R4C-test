from django.urls import path
from robots import views

urlpatterns = [
    path("new", views.AddRobotView.as_view(), name="new_robot"),
]