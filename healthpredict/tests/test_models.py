"""
Model tests
"""
import pytest
from django.contrib.auth import get_user_model
from predictor.models import PatientProfile, HealthAssessment, PredictionResult
from tests.factories import UserFactory, PatientProfileFactory, HealthAssessmentFactory

User = get_user_model()


@pytest.mark.unit
@pytest.mark.django_db
class TestPatientProfile:
    """Test PatientProfile model"""
    
    def test_create_patient_profile(self, user):
        """Test creating a patient profile"""
        profile = PatientProfile.objects.create(
            user=user,
            date_of_birth='1990-01-01',
            gender='male',
            blood_group='O+',
            height=175.0,
            weight=75.0
        )
        
        assert profile.user == user
        assert profile.gender == 'male'
        assert profile.blood_group == 'O+'
    
    def test_patient_profile_bmi_calculation(self, user):
        """Test BMI calculation"""
        profile = PatientProfile.objects.create(
            user=user,
            height=175.0,  # 1.75m
            weight=75.0    # 75kg
        )
        
        # BMI = weight / (height^2) = 75 / (1.75^2) ≈ 24.49
        assert profile.bmi is not None
        assert 24 < profile.bmi < 25
    
    def test_patient_profile_age_calculation(self, user):
        """Test age calculation"""
        profile = PatientProfile.objects.create(
            user=user,
            date_of_birth='1990-01-01'
        )
        
        assert profile.age is not None
        assert profile.age >= 30  # As of 2024
    
    def test_patient_profile_factory(self):
        """Test patient profile factory"""
        profile = PatientProfileFactory()
        
        assert profile.user is not None
        assert profile.gender in ['male', 'female', 'other']
        assert profile.height > 0
        assert profile.weight > 0


@pytest.mark.unit
@pytest.mark.django_db
class TestHealthAssessment:
    """Test HealthAssessment model"""
    
    def test_create_health_assessment(self, patient_profile, user):
        """Test creating a health assessment"""
        assessment = HealthAssessment.objects.create(
            patient=patient_profile,
            assessed_by=user,
            systolic_bp=120,
            diastolic_bp=80,
            heart_rate=72,
            fasting_glucose=95,
            total_cholesterol=180,
            status='completed'
        )
        
        assert assessment.patient == patient_profile
        assert assessment.assessed_by == user
        assert assessment.status == 'completed'
    
    def test_health_assessment_factory(self):
        """Test health assessment factory"""
        assessment = HealthAssessmentFactory()
        
        assert assessment.patient is not None
        assert assessment.systolic_bp > 0
        assert assessment.diastolic_bp > 0
        assert assessment.status == 'completed'


@pytest.mark.unit
@pytest.mark.django_db
class TestPredictionResult:
    """Test PredictionResult model"""
    
    def test_create_prediction_result(self, health_assessment):
        """Test creating a prediction result"""
        prediction = PredictionResult.objects.create(
            assessment=health_assessment,
            heart_disease_risk=25.5,
            diabetes_risk=15.2,
            cancer_risk=10.8,
            stroke_risk=12.1,
            heart_disease_category='low',
            diabetes_category='low',
            cancer_category='low',
            stroke_category='low',
            model_version='1.0.0'
        )
        
        assert prediction.assessment == health_assessment
        assert prediction.heart_disease_risk == 25.5
        assert prediction.heart_disease_category == 'low'
    
    def test_overall_risk_score_calculation(self, health_assessment):
        """Test overall risk score calculation"""
        prediction = PredictionResult.objects.create(
            assessment=health_assessment,
            heart_disease_risk=50.0,
            diabetes_risk=40.0,
            cancer_risk=30.0,
            stroke_risk=20.0,
            model_version='1.0.0'
        )
        
        # Overall risk should be the maximum of all risks
        assert prediction.overall_risk_score == 50.0
    
    def test_primary_risk_condition(self, health_assessment):
        """Test primary risk condition identification"""
        prediction = PredictionResult.objects.create(
            assessment=health_assessment,
            heart_disease_risk=70.0,
            diabetes_risk=40.0,
            cancer_risk=30.0,
            stroke_risk=20.0,
            model_version='1.0.0'
        )
        
        # Primary risk should be heart disease (highest risk)
        assert 'heart' in prediction.primary_risk_condition.lower()
