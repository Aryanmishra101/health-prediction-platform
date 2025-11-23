from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import json

class PatientProfile(models.Model):
    """Extended user profile for health prediction platform"""
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say'),
    ]
    
    SMOKING_CHOICES = [
        ('never', 'Never smoked'),
        ('former', 'Former smoker'),
        ('current', 'Current smoker'),
    ]
    
    ALCOHOL_CHOICES = [
        ('never', 'Never drink'),
        ('occasional', 'Occasional drinker'),
        ('moderate', 'Moderate drinker'),
        ('heavy', 'Heavy drinker'),
    ]
    
    EXERCISE_CHOICES = [
        ('sedentary', 'Sedentary'),
        ('light', 'Light activity'),
        ('moderate', 'Moderate activity'),
        ('vigorous', 'Vigorous activity'),
    ]
    
    FAMILY_HISTORY_CHOICES = [
        ('none', 'No family history'),
        ('heart_disease', 'Heart disease'),
        ('diabetes', 'Diabetes'),
        ('cancer', 'Cancer'),
        ('multiple', 'Multiple conditions'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    medical_id = models.CharField(max_length=20, unique=True, blank=True)
    
    # Lifestyle factors
    smoking_status = models.CharField(max_length=20, choices=SMOKING_CHOICES, default='never')
    alcohol_consumption = models.CharField(max_length=20, choices=ALCOHOL_CHOICES, default='never')
    exercise_level = models.CharField(max_length=20, choices=EXERCISE_CHOICES, default='sedentary')
    family_medical_history = models.CharField(max_length=20, choices=FAMILY_HISTORY_CHOICES, default='none')
    
    # Medical information
    height = models.FloatField(null=True, blank=True, validators=[MinValueValidator(100), MaxValueValidator(250)])
    weight = models.FloatField(null=True, blank=True, validators=[MinValueValidator(30), MaxValueValidator(300)])
    blood_type = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.medical_id}"
    
    @property
    def age(self):
        """Calculate patient age"""
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    @property
    def bmi(self):
        """Calculate BMI"""
        if self.height and self.weight:
            height_m = self.height / 100
            return round(self.weight / (height_m ** 2), 1)
        return None


class HealthAssessment(models.Model):
    """Health assessment data for ML predictions"""
    
    ASSESSMENT_STATUS = [
        ('draft', 'Draft'),
        ('completed', 'Completed'),
        ('reviewed', 'Reviewed'),
        ('archived', 'Archived'),
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    assessment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ASSESSMENT_STATUS, default='draft')
    
    # Vital signs and measurements
    systolic_bp = models.IntegerField(validators=[MinValueValidator(70), MaxValueValidator(250)])
    diastolic_bp = models.IntegerField(validators=[MinValueValidator(40), MaxValueValidator(150)])
    heart_rate = models.IntegerField(validators=[MinValueValidator(40), MaxValueValidator(200)])
    temperature = models.FloatField(validators=[MinValueValidator(30), MaxValueValidator(45)])
    
    # Laboratory results
    total_cholesterol = models.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(400)])
    hdl_cholesterol = models.IntegerField(validators=[MinValueValidator(20), MaxValueValidator(100)])
    ldl_cholesterol = models.IntegerField(validators=[MinValueValidator(50), MaxValueValidator(300)])
    triglycerides = models.IntegerField(validators=[MinValueValidator(50), MaxValueValidator(1000)])
    fasting_glucose = models.IntegerField(validators=[MinValueValidator(70), MaxValueValidator(500)])
    hba1c = models.FloatField(validators=[MinValueValidator(4.0), MaxValueValidator(15.0)])
    creatinine = models.FloatField(validators=[MinValueValidator(0.3), MaxValueValidator(5.0)])
    hemoglobin = models.FloatField(validators=[MinValueValidator(8.0), MaxValueValidator(20.0)])
    
    # Symptoms and clinical indicators
    chest_pain = models.BooleanField(default=False)
    shortness_of_breath = models.BooleanField(default=False)
    fatigue = models.BooleanField(default=False)
    frequent_urination = models.BooleanField(default=False)
    excessive_thirst = models.BooleanField(default=False)
    unexplained_weight_loss = models.BooleanField(default=False)
    blurred_vision = models.BooleanField(default=False)
    dizziness = models.BooleanField(default=False)
    palpitations = models.BooleanField(default=False)
    
    # Additional clinical data
    stress_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=5)
    sleep_hours = models.FloatField(validators=[MinValueValidator(3), MaxValueValidator(12)], default=7)
    
    # Assessment metadata
    assessed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assessments_conducted')
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-assessment_date']
    
    def __str__(self):
        return f"Assessment {self.id} - {self.patient.user.get_full_name()} - {self.assessment_date.strftime('%Y-%m-%d')}"


class PredictionResult(models.Model):
    """Machine learning prediction results"""
    
    assessment = models.OneToOneField(HealthAssessment, on_delete=models.CASCADE)
    prediction_date = models.DateTimeField(auto_now_add=True)
    
    # Risk scores (0-100)
    heart_disease_risk = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    diabetes_risk = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    cancer_risk = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    stroke_risk = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Prediction confidence scores
    heart_disease_confidence = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    diabetes_confidence = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    cancer_confidence = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    stroke_confidence = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # Risk categories
    RISK_CATEGORIES = [
        ('low', 'Low Risk'),
        ('moderate', 'Moderate Risk'),
        ('high', 'High Risk'),
        ('very_high', 'Very High Risk'),
    ]
    
    heart_disease_category = models.CharField(max_length=20, choices=RISK_CATEGORIES)
    diabetes_category = models.CharField(max_length=20, choices=RISK_CATEGORIES)
    cancer_category = models.CharField(max_length=20, choices=RISK_CATEGORIES)
    stroke_category = models.CharField(max_length=20, choices=RISK_CATEGORIES)
    
    # Feature importance (JSON field for storing feature contributions)
    feature_importance = models.JSONField(default=dict)
    
    # Model information
    model_version = models.CharField(max_length=20, default='1.0.0')
    prediction_time_ms = models.FloatField()
    
    # Clinical recommendations
    recommendations = models.JSONField(default=list)
    follow_up_required = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-prediction_date']
    
    def __str__(self):
        return f"Prediction {self.id} - {self.assessment.patient.user.get_full_name()}"
    
    @property
    def overall_risk_score(self):
        """Calculate overall risk score"""
        return max(self.heart_disease_risk, self.diabetes_risk, self.cancer_risk, self.stroke_risk)
    
    @property
    def primary_risk_condition(self):
        """Identify the primary risk condition"""
        risks = {
            'Heart Disease': self.heart_disease_risk,
            'Diabetes': self.diabetes_risk,
            'Cancer': self.cancer_risk,
            'Stroke': self.stroke_risk
        }
        return max(risks, key=risks.get)


class MedicalHistory(models.Model):
    """Patient medical history and conditions"""
    
    CONDITION_TYPES = [
        ('cardiovascular', 'Cardiovascular'),
        ('endocrine', 'Endocrine'),
        ('respiratory', 'Respiratory'),
        ('gastrointestinal', 'Gastrointestinal'),
        ('neurological', 'Neurological'),
        ('psychiatric', 'Psychiatric'),
        ('musculoskeletal', 'Musculoskeletal'),
        ('other', 'Other'),
    ]
    
    SEVERITY_LEVELS = [
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('severe', 'Severe'),
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medical_history')
    condition_name = models.CharField(max_length=100)
    condition_type = models.CharField(max_length=20, choices=CONDITION_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    diagnosis_date = models.DateField()
    is_active = models.BooleanField(default=True)
    treatment_description = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-diagnosis_date']
    
    def __str__(self):
        return f"{self.condition_name} - {self.patient.user.get_full_name()}"


class LifestyleMetric(models.Model):
    """Track lifestyle metrics over time"""
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='lifestyle_metrics')
    metric_date = models.DateField()
    
    # Physical activity
    steps_per_day = models.IntegerField(null=True, blank=True)
    exercise_minutes = models.IntegerField(null=True, blank=True)
    active_hours = models.FloatField(null=True, blank=True)
    
    # Nutrition
    calorie_intake = models.IntegerField(null=True, blank=True)
    water_intake_liters = models.FloatField(null=True, blank=True)
    fruit_servings = models.IntegerField(null=True, blank=True)
    vegetable_servings = models.IntegerField(null=True, blank=True)
    
    # Sleep and wellness
    sleep_quality = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True)
    stress_level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True)
    mood_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True)
    
    # Substance use
    cigarettes_per_day = models.IntegerField(null=True, blank=True)
    alcohol_units_per_week = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-metric_date']
    
    def __str__(self):
        return f"Lifestyle {self.metric_date} - {self.patient.user.get_full_name()}"


class MedicalReport(models.Model):
    """Stores uploaded medical reports for OCR processing"""
    
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF Document'),
        ('jpg', 'JPEG Image'),
        ('jpeg', 'JPEG Image'),
        ('png', 'PNG Image'),
    ]
    
    PROCESSING_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medical_reports')
    file = models.FileField(upload_to='medical_reports/%Y/%m/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    file_size = models.IntegerField(help_text='File size in bytes')
    original_filename = models.CharField(max_length=255)
    
    # Processing metadata
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processing_status = models.CharField(max_length=20, choices=PROCESSING_STATUS, default='pending')
    processing_error = models.TextField(blank=True)
    
    # Extracted data stored as JSON
    extracted_data = models.JSONField(null=True, blank=True, help_text='OCR extracted medical data')
    extraction_confidence = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(1)])
    
    # Link to created assessment if auto-filled
    health_assessment = models.ForeignKey(
        HealthAssessment, 
        null=True, 
        blank=True,
        on_delete=models.SET_NULL,
        related_name='source_report'
    )
    
    # Privacy and security
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"Report {self.id} - {self.patient.user.get_full_name()} - {self.uploaded_at.strftime('%Y-%m-%d')}"
    
    @property
    def file_size_mb(self):
        """Return file size in MB"""
        return round(self.file_size / (1024 * 1024), 2)
    
    def soft_delete(self):
        """Soft delete the report"""
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()