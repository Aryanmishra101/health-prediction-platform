"""
Pytest configuration and fixtures for Health Prediction Platform tests
"""
import pytest
from django.contrib.auth import get_user_model
from predictor.models import PatientProfile, HealthAssessment, PredictionResult

User = get_user_model()


@pytest.fixture
def user(db):
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Test',
        last_name='User'
    )


@pytest.fixture
def authenticated_client(client, user):
    """Create an authenticated client"""
    client.force_login(user)
    return client


@pytest.fixture
def patient_profile(db, user):
    """Create a test patient profile"""
    return PatientProfile.objects.create(
        user=user,
        date_of_birth='1990-01-01',
        gender='male',
        blood_group='O+',
        height=175.0,
        weight=75.0,
        smoking_status='never',
        alcohol_consumption='occasional',
        exercise_level='moderate',
        family_medical_history={'heart_disease': True}
    )


@pytest.fixture
def health_assessment(db, patient_profile, user):
    """Create a test health assessment"""
    return HealthAssessment.objects.create(
        patient=patient_profile,
        assessed_by=user,
        systolic_bp=120,
        diastolic_bp=80,
        heart_rate=72,
        fasting_glucose=95,
        total_cholesterol=180,
        hdl_cholesterol=50,
        ldl_cholesterol=110,
        triglycerides=100,
        hba1c=5.5,
        creatinine=1.0,
        hemoglobin=15.0,
        status='completed'
    )


@pytest.fixture
def prediction_result(db, health_assessment):
    """Create a test prediction result"""
    return PredictionResult.objects.create(
        assessment=health_assessment,
        heart_disease_risk=25.5,
        diabetes_risk=15.2,
        cancer_risk=10.8,
        stroke_risk=12.1,
        heart_disease_confidence=0.85,
        diabetes_confidence=0.82,
        cancer_confidence=0.78,
        stroke_confidence=0.80,
        heart_disease_category='low',
        diabetes_category='low',
        cancer_category='low',
        stroke_category='low',
        model_version='1.0.0',
        recommendations=['Maintain healthy lifestyle', 'Regular exercise']
    )


@pytest.fixture
def sample_health_data():
    """Sample health data for predictions"""
    return {
        'age': 45,
        'gender': 'male',
        'bmi': 26.5,
        'systolic_bp': 130,
        'diastolic_bp': 85,
        'heart_rate': 75,
        'fasting_glucose': 105,
        'total_cholesterol': 210,
        'hdl_cholesterol': 45,
        'ldl_cholesterol': 140,
        'triglycerides': 150,
        'hba1c': 5.8,
        'creatinine': 1.1,
        'hemoglobin': 14.5,
        'smoking_status': 'former',
        'alcohol_consumption': 'moderate',
        'exercise_level': 'low',
        'family_medical_history': {'diabetes': True, 'heart_disease': True}
    }
