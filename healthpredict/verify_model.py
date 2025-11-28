import os
import sys
import django
import logging

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthpredict.settings')
django.setup()

from predictor.ml_models import health_predictor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_model():
    logger.info("Verifying retrained model...")
    
    # Check if model is loaded
    if health_predictor.model is None:
        logger.error("Model failed to load!")
        return
        
    logger.info(f"Model version: {health_predictor.model_version}")
    
    # Test prediction
    test_data = {
        'age': 45,
        'gender': 'male',
        'bmi': 28.5,
        'systolic_bp': 130,
        'diastolic_bp': 85,
        'total_cholesterol': 210,
        'fasting_glucose': 105,
        'smoking_status': 'former',
        'alcohol_consumption': 'occasional',
        'exercise_level': 'moderate'
    }
    
    try:
        results = health_predictor.predict_health_risks(test_data)
        logger.info("Prediction successful!")
        logger.info(f"Results: {results}")
        
        # Basic validation
        assert 'heart_disease_risk' in results
        assert 'diabetes_risk' in results
        assert 'cancer_risk' in results
        assert 'stroke_risk' in results
        
        print("\nVerification Passed: Model loaded and generated predictions.")
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise

if __name__ == "__main__":
    verify_model()
