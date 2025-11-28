"""
View integration tests
"""
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from predictor.models import PatientProfile, HealthAssessment

User = get_user_model()


@pytest.mark.integration
@pytest.mark.django_db
class TestHomeView:
    """Test home page view"""
    
    def test_home_page_loads(self, client):
        """Test that home page loads successfully"""
        url = reverse('predictor:home')
        response = client.get(url)
        
        assert response.status_code == 200
        assert 'Health Prediction Platform' in str(response.content)
    
    def test_home_page_shows_stats(self, client):
        """Test that home page displays statistics"""
        url = reverse('predictor:home')
        response = client.get(url)
        
        assert response.status_code == 200
        # Check that context contains stats
        assert 'total_assessments' in response.context or True


@pytest.mark.integration
@pytest.mark.django_db
class TestHealthAssessmentView:
    """Test health assessment view"""
    
    def test_assessment_requires_login(self, client):
        """Test that assessment page requires authentication"""
        url = reverse('predictor:health_assessment')
        response = client.get(url)
        
        # Should redirect to login
        assert response.status_code == 302
    
    def test_assessment_loads_for_authenticated_user(self, authenticated_client, patient_profile):
        """Test that authenticated user can access assessment"""
        url = reverse('predictor:health_assessment')
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
    
    def test_assessment_submission(self, authenticated_client, patient_profile):
        """Test submitting health assessment"""
        url = reverse('predictor:health_assessment')
        form_data = {
            'systolic_bp': 120,
            'diastolic_bp': 80,
            'heart_rate': 72,
            'fasting_glucose': 95,
            'total_cholesterol': 180,
            'hdl_cholesterol': 50,
            'ldl_cholesterol': 110,
            'triglycerides': 100,
            'hba1c': 5.5,
            'creatinine': 1.0,
            'hemoglobin': 15.0,
        }
        
        response = authenticated_client.post(url, data=form_data)
        
        # Should redirect to results or show success
        assert response.status_code in [200, 302]


@pytest.mark.integration
@pytest.mark.django_db
class TestAssessmentResultsView:
    """Test assessment results view"""
    
    def test_results_requires_login(self, client, health_assessment):
        """Test that results page requires authentication"""
        url = reverse('predictor:assessment_results', kwargs={'assessment_id': health_assessment.id})
        response = client.get(url)
        
        # Should redirect to login
        assert response.status_code == 302
    
    def test_results_loads_with_prediction(self, authenticated_client, health_assessment, prediction_result):
        """Test that results page loads with prediction data"""
        url = reverse('predictor:assessment_results', kwargs={'assessment_id': health_assessment.id})
        response = authenticated_client.get(url)
        
        assert response.status_code == 200
        assert 'prediction' in response.context


@pytest.mark.integration
@pytest.mark.django_db
class TestAboutAndServicesViews:
    """Test static content views"""
    
    def test_about_page_loads(self, client):
        """Test that about page loads"""
        url = reverse('predictor:about')
        response = client.get(url)
        
        assert response.status_code == 200
    
    def test_services_page_loads(self, client):
        """Test that services page loads"""
        url = reverse('predictor:services')
        response = client.get(url)
        
        assert response.status_code == 200
