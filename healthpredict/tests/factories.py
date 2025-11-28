"""
Factory classes for generating test data
"""
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from predictor.models import PatientProfile, HealthAssessment, PredictionResult
from faker import Faker

fake = Faker()
User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    is_active = True


class PatientProfileFactory(DjangoModelFactory):
    class Meta:
        model = PatientProfile
    
    user = factory.SubFactory(UserFactory)
    date_of_birth = factory.Faker('date_of_birth', minimum_age=18, maximum_age=90)
    gender = factory.Iterator(['male', 'female', 'other'])
    blood_group = factory.Iterator(['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'])
    height = factory.Faker('pyfloat', min_value=150, max_value=200)
    weight = factory.Faker('pyfloat', min_value=50, max_value=120)
    smoking_status = factory.Iterator(['never', 'former', 'current'])
    alcohol_consumption = factory.Iterator(['never', 'occasional', 'moderate', 'heavy'])
    exercise_level = factory.Iterator(['sedentary', 'low', 'moderate', 'high'])


class HealthAssessmentFactory(DjangoModelFactory):
    class Meta:
        model = HealthAssessment
    
    patient = factory.SubFactory(PatientProfileFactory)
    assessed_by = factory.LazyAttribute(lambda obj: obj.patient.user)
    systolic_bp = factory.Faker('pyint', min_value=90, max_value=180)
    diastolic_bp = factory.Faker('pyint', min_value=60, max_value=120)
    heart_rate = factory.Faker('pyint', min_value=50, max_value=120)
    fasting_glucose = factory.Faker('pyint', min_value=70, max_value=200)
    total_cholesterol = factory.Faker('pyint', min_value=120, max_value=300)
    hdl_cholesterol = factory.Faker('pyint', min_value=30, max_value=80)
    ldl_cholesterol = factory.Faker('pyint', min_value=50, max_value=200)
    triglycerides = factory.Faker('pyint', min_value=50, max_value=300)
    hba1c = factory.Faker('pyfloat', min_value=4.0, max_value=10.0)
    creatinine = factory.Faker('pyfloat', min_value=0.5, max_value=2.0)
    hemoglobin = factory.Faker('pyfloat', min_value=10.0, max_value=18.0)
    status = 'completed'


class PredictionResultFactory(DjangoModelFactory):
    class Meta:
        model = PredictionResult
    
    assessment = factory.SubFactory(HealthAssessmentFactory)
    heart_disease_risk = factory.Faker('pyfloat', min_value=0, max_value=100)
    diabetes_risk = factory.Faker('pyfloat', min_value=0, max_value=100)
    cancer_risk = factory.Faker('pyfloat', min_value=0, max_value=100)
    stroke_risk = factory.Faker('pyfloat', min_value=0, max_value=100)
    heart_disease_confidence = factory.Faker('pyfloat', min_value=0.7, max_value=0.95)
    diabetes_confidence = factory.Faker('pyfloat', min_value=0.7, max_value=0.95)
    cancer_confidence = factory.Faker('pyfloat', min_value=0.7, max_value=0.95)
    stroke_confidence = factory.Faker('pyfloat', min_value=0.7, max_value=0.95)
    model_version = '1.0.0'
