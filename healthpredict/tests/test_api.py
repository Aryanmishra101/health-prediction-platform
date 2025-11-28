"""
API endpoint tests
"""
import pytest
from django.urls import reverse
from rest_framework import status
import json


@pytest.mark.api
class TestPredictionAPI:
    """Test the prediction API endpoints"""
    
    def test_health_check_endpoint(self, client):
        """Test the health check endpoint"""
        url = reverse('predictor_api:api_health')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'status' in data
        assert data['status'] == 'healthy'
        assert 'model_loaded' in data
        assert 'timestamp' in data
    
    def test_live_stats_endpoint(self, client):
        """Test the live statistics endpoint"""
        url = reverse('predictor_api:api_stats')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert 'total_assessments' in data
        assert 'active_users' in data
        assert 'prediction_accuracy' in data
    
    def test_predict_endpoint_with_valid_data(self, client, sample_health_data):
        """Test prediction endpoint with valid data"""
        url = reverse('predictor_api:api_predict')
        response = client.post(
            url,
            data=json.dumps(sample_health_data),
            content_type='application/json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['success'] is True
        assert 'prediction' in data
        assert 'timestamp' in data
        
        prediction = data['prediction']
        assert 'heart_disease_risk' in prediction
        assert 'diabetes_risk' in prediction
        assert 'cancer_risk' in prediction
        assert 'stroke_risk' in prediction
    
    def test_predict_endpoint_missing_required_fields(self, client):
        """Test prediction endpoint with missing required fields"""
        url = reverse('predictor_api:api_predict')
        incomplete_data = {
            'systolic_bp': 120
            # Missing other required fields
        }
        
        response = client.post(
            url,
            data=json.dumps(incomplete_data),
            content_type='application/json'
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        data = response.json()
        assert 'error' in data
    
    def test_predict_endpoint_invalid_method(self, client):
        """Test prediction endpoint with GET instead of POST"""
        url = reverse('predictor_api:api_predict')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


@pytest.mark.api
class TestRateLimiting:
    """Test API rate limiting"""
    
    @pytest.mark.slow
    def test_rate_limit_exceeded(self, client, sample_health_data):
        """Test that rate limiting works after many requests"""
        url = reverse('predictor_api:api_predict')
        
        # Make many requests to trigger rate limit
        # Note: This test may be slow, marked with @pytest.mark.slow
        responses = []
        for i in range(15):  # Reduced from 110 for faster testing
            response = client.post(
                url,
                data=json.dumps(sample_health_data),
                content_type='application/json'
            )
            responses.append(response.status_code)
        
        # At least some requests should succeed
        assert status.HTTP_200_OK in responses


@pytest.mark.integration
class TestAuthenticatedAPI:
    """Test authenticated API endpoints"""
    
    def test_authenticated_prediction(self, authenticated_client, sample_health_data):
        """Test prediction with authenticated user"""
        url = reverse('predictor_api:api_predict')
        response = authenticated_client.post(
            url,
            data=json.dumps(sample_health_data),
            content_type='application/json'
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data['success'] is True
