from django.urls import path
from robots import views

urlpatterns = [
    path('report', views.ReportView.as_view(), name="report"),
    path('report/<str:filename>/', views.download_report, name='download_report'),
]
