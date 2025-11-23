"""
URL patterns for the predictor app
"""

from django.urls import path
from . import views

app_name = 'predictor'

urlpatterns = [
    # Main pages
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    
    # Assessment URLs
    path('assessment/', views.health_assessment_view, name='health_assessment'),
    path('assessment/results/<int:assessment_id>/', views.assessment_results_view, name='assessment_results'),
    path('assessment/history/', views.assessment_history_view, name='assessment_history'),
    path('assessment/export/<int:assessment_id>/', views.export_results_view, name='export_results'),
    
    # Medical Report Upload URLs
    path('upload-report/', views.upload_medical_report, name='upload_report'),
    path('process-report/<int:report_id>/', views.process_medical_report, name='process_report'),
    path('delete-report/<int:report_id>/', views.delete_medical_report, name='delete_report'),
]