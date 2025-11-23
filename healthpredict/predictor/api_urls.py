"""
API URL patterns for the predictor app
"""

from django.urls import path
from . import views

app_name = 'predictor_api'

urlpatterns = [
    path('predict/', views.api_predict_view, name='api_predict'),
    path('health/', views.api_health_check, name='api_health'),
]