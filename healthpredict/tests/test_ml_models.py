"""
Unit tests for ML models
"""
import pytest
from predictor.ml_models import health_predictor


@pytest.mark.unit
class TestHealthPredictor:
    """Test the health prediction ML model"""
    
    def test_model_loaded(self):
        """Test that the model is loaded successfully"""
        assert health_predictor.model is not None
        assert health_predictor.scaler is not None
    
    def test_predict_health_risks(self, sample_health_data):
        """Test health risk prediction with valid data"""
        results = health_predictor.predict_health_risks(sample_health_data)
        
        # Check that all risk scores are present
        assert 'heart_disease_risk' in results
        assert 'diabetes_risk' in results
        assert 'cancer_risk' in results
        assert 'stroke_risk' in results
        
        # Check that risk scores are in valid range (0-100)
        assert 0 <= results['heart_disease_risk'] <= 100
        assert 0 <= results['diabetes_risk'] <= 100
        assert 0 <= results['cancer_risk'] <= 100
        assert 0 <= results['stroke_risk'] <= 100
        
        # Check that categories are assigned
        assert results['heart_disease_category'] in ['low', 'moderate', 'high', 'very_high']
        assert results['diabetes_category'] in ['low', 'moderate', 'high', 'very_high']
        assert results['cancer_category'] in ['low', 'moderate', 'high', 'very_high']
        assert results['stroke_category'] in ['low', 'moderate', 'high', 'very_high']
    
    def test_predict_with_minimal_data(self):
        """Test prediction with minimal required data"""
        minimal_data = {
            'systolic_bp': 120,
            'diastolic_bp': 80,
            'fasting_glucose': 100,
            'total_cholesterol': 200
        }
        
        results = health_predictor.predict_health_risks(minimal_data)
        assert 'heart_disease_risk' in results
        assert 'diabetes_risk' in results
    
    def test_predict_high_risk_patient(self):
        """Test prediction for high-risk patient"""
        high_risk_data = {
            'age': 65,
            'gender': 'male',
            'bmi': 35.0,
            'systolic_bp': 160,
            'diastolic_bp': 100,
            'fasting_glucose': 180,
            'total_cholesterol': 280,
            'hdl_cholesterol': 30,
            'ldl_cholesterol': 200,
            'triglycerides': 250,
            'hba1c': 8.5,
            'smoking_status': 'current',
            'exercise_level': 'sedentary'
        }
        
        results = health_predictor.predict_health_risks(high_risk_data)
        
        # High risk patient should have elevated risk scores
        assert results['heart_disease_risk'] > 30 or results['diabetes_risk'] > 30
    
    def test_predict_low_risk_patient(self):
        """Test prediction for low-risk patient"""
        low_risk_data = {
            'age': 25,
            'gender': 'female',
            'bmi': 22.0,
            'systolic_bp': 110,
            'diastolic_bp': 70,
            'fasting_glucose': 85,
            'total_cholesterol': 160,
            'hdl_cholesterol': 60,
            'ldl_cholesterol': 90,
            'triglycerides': 80,
            'hba1c': 5.0,
            'smoking_status': 'never',
            'exercise_level': 'high'
        }
        
        results = health_predictor.predict_health_risks(low_risk_data)
        
        # Low risk patient should have lower risk scores
        assert results['heart_disease_risk'] < 50
        assert results['diabetes_risk'] < 50
    
    def test_recommendations_generated(self, sample_health_data):
        """Test that recommendations are generated"""
        results = health_predictor.predict_health_risks(sample_health_data)
        
        assert 'recommendations' in results
        assert isinstance(results['recommendations'], list)
        assert len(results['recommendations']) > 0
    
    def test_model_version_included(self, sample_health_data):
        """Test that model version is included in results"""
        results = health_predictor.predict_health_risks(sample_health_data)
        
        assert 'model_version' in results
        assert results['model_version'] is not None
    
    def test_prediction_time_tracked(self, sample_health_data):
        """Test that prediction time is tracked"""
        results = health_predictor.predict_health_risks(sample_health_data)
        
        assert 'prediction_time_ms' in results
        assert results['prediction_time_ms'] >= 0
