"""
URL patterns for the dashboard app
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.AnalyticsDashboardView.as_view(), name='analytics'),
    path('reports/', views.ReportsView.as_view(), name='reports'),
    path('api/analytics/', views.analytics_data_view, name='analytics_data'),
    path('api/risk_distribution/', views.risk_distribution_view, name='risk_distribution'),
]