"""
API URL patterns for the predictor app
"""

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

app_name = 'predictor_api'

urlpatterns = [
    path('predict/', views.api_predict_view, name='api_predict'),
    path('health/', views.api_health_check, name='api_health'),
    path('stats/', views.get_live_stats, name='api_stats'),
    
    # API Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='predictor_api:schema'), name='swagger-ui'),
]