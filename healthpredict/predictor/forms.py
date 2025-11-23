"""
Forms for the predictor app
Health assessment and patient profile forms
"""

from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import HealthAssessment, PatientProfile

class HealthAssessmentForm(forms.ModelForm):
    """Health assessment form with medical-grade validation"""
    
    class Meta:
        model = HealthAssessment
        fields = [
            'systolic_bp', 'diastolic_bp', 'heart_rate', 'temperature',
            'total_cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
            'fasting_glucose', 'hba1c', 'creatinine', 'hemoglobin',
            'chest_pain', 'shortness_of_breath', 'fatigue', 'frequent_urination',
            'excessive_thirst', 'unexplained_weight_loss', 'blurred_vision',
            'dizziness', 'palpitations', 'stress_level', 'sleep_hours', 'notes'
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional notes or symptoms...'}),
            'chest_pain': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'shortness_of_breath': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fatigue': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'frequent_urination': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'excessive_thirst': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'unexplained_weight_loss': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'blurred_vision': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dizziness': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'palpitations': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add Bootstrap classes and placeholders
        for field_name, field in self.fields.items():
            if isinstance(field, forms.IntegerField):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'type': 'number',
                    'min': field.validators[0].limit_value if field.validators else 0,
                    'max': field.validators[1].limit_value if len(field.validators) > 1 else 1000
                })
            elif isinstance(field, forms.FloatField):
                field.widget.attrs.update({
                    'class': 'form-control',
                    'type': 'number',
                    'step': '0.1',
                    'min': field.validators[0].limit_value if field.validators else 0,
                    'max': field.validators[1].limit_value if len(field.validators) > 1 else 100
                })
            elif isinstance(field, forms.CharField) and field_name != 'notes':
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field, forms.ChoiceField):
                field.widget.attrs.update({'class': 'form-select'})
            
            # Make boolean fields optional (unchecked = False)
            if isinstance(field, forms.BooleanField):
                field.required = False
    
    def clean(self):
        """Custom validation for medical consistency"""
        cleaned_data = super().clean()
        
        # Blood pressure validation
        systolic = cleaned_data.get('systolic_bp')
        diastolic = cleaned_data.get('diastolic_bp')
        
        if systolic and diastolic:
            if systolic <= diastolic:
                self.add_error('systolic_bp', 'Systolic pressure must be higher than diastolic pressure')
            
            if systolic > 200 or diastolic > 120:
                self.add_error(None, 'Critical blood pressure values detected. Seek immediate medical attention.')
        
        # Cholesterol validation
        total_chol = cleaned_data.get('total_cholesterol')
        hdl_chol = cleaned_data.get('hdl_cholesterol')
        ldl_chol = cleaned_data.get('ldl_cholesterol')
        
        if all([total_chol, hdl_chol, ldl_chol]):
            if total_chol < (hdl_chol + ldl_chol):
                self.add_error('total_cholesterol', 'Total cholesterol should be greater than HDL + LDL')
        
        # Glucose validation
        glucose = cleaned_data.get('fasting_glucose')
        hba1c = cleaned_data.get('hba1c')
        
        if glucose and glucose > 300:
            self.add_error('fasting_glucose', 'Critical glucose level detected. Seek immediate medical attention.')
        
        if hba1c and hba1c > 12:
            self.add_error('hba1c', 'Poorly controlled diabetes. Consult healthcare provider immediately.')
        
        # Heart rate validation
        heart_rate = cleaned_data.get('heart_rate')
        if heart_rate:
            if heart_rate < 40:
                self.add_error('heart_rate', 'Bradycardia detected. Consult healthcare provider.')
            elif heart_rate > 150:
                self.add_error('heart_rate', 'Tachycardia detected. Consult healthcare provider.')
        
        return cleaned_data

class PatientProfileForm(forms.ModelForm):
    """Patient profile setup form"""
    
    class Meta:
        model = PatientProfile
        fields = [
            'date_of_birth', 'gender', 'phone', 'emergency_contact', 'height', 'weight',
            'blood_type', 'allergies', 'current_medications', 'smoking_status',
            'alcohol_consumption', 'exercise_level', 'family_medical_history'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name and phone number'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'cm', 'min': 100, 'max': 250}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'kg', 'min': 30, 'max': 300}),
            'blood_type': forms.Select(attrs={'class': 'form-select'}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'List any known allergies...'}),
            'current_medications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List current medications, dosages, and frequency...'}),
            'smoking_status': forms.Select(attrs={'class': 'form-select'}),
            'alcohol_consumption': forms.Select(attrs={'class': 'form-select'}),
            'exercise_level': forms.Select(attrs={'class': 'form-select'}),
            'family_medical_history': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add blood type choices
        self.fields['blood_type'].choices = [
            ('', 'Select blood type'),
            ('O+', 'O Positive (O+)'),
            ('O-', 'O Negative (O-)'),
            ('A+', 'A Positive (A+)'),
            ('A-', 'A Negative (A-)'),
            ('B+', 'B Positive (B+)'),
            ('B-', 'B Negative (B-)'),
            ('AB+', 'AB Positive (AB+)'),
            ('AB-', 'AB Negative (AB-)'),
        ]
    
    def clean(self):
        """Custom validation for patient profile"""
        cleaned_data = super().clean()
        
        # Age validation
        date_of_birth = cleaned_data.get('date_of_birth')
        if date_of_birth:
            from datetime import date
            age = date.today().year - date_of_birth.year
            if age < 18:
                self.add_error('date_of_birth', 'Patient must be 18 years or older')
            elif age > 120:
                self.add_error('date_of_birth', 'Please verify the date of birth')
        
        # BMI validation
        height = cleaned_data.get('height')
        weight = cleaned_data.get('weight')
        
        if height and weight:
            bmi = weight / ((height / 100) ** 2)
            if bmi < 15 or bmi > 50:
                self.add_error('weight', f'BMI of {bmi:.1f} is outside normal range. Please verify measurements.')
        
        return cleaned_data

class QuickAssessmentForm(forms.Form):
    """Quick health assessment form for rapid screening"""
    
    age = forms.IntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(120)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'})
    )
    
    gender = forms.ChoiceField(
        choices=[('male', 'Male'), ('female', 'Female')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    height = forms.FloatField(
        validators=[MinValueValidator(100), MaxValueValidator(250)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Height (cm)'})
    )
    
    weight = forms.FloatField(
        validators=[MinValueValidator(30), MaxValueValidator(300)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight (kg)'})
    )
    
    systolic_bp = forms.IntegerField(
        validators=[MinValueValidator(70), MaxValueValidator(250)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Systolic BP'})
    )
    
    diastolic_bp = forms.IntegerField(
        validators=[MinValueValidator(40), MaxValueValidator(150)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Diastolic BP'})
    )
    
    fasting_glucose = forms.IntegerField(
        validators=[MinValueValidator(70), MaxValueValidator(500)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Fasting Glucose'})
    )
    
    total_cholesterol = forms.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(400)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Cholesterol'})
    )
    
    smoking = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    family_history = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    def clean(self):
        """Validation for quick assessment"""
        cleaned_data = super().clean()
        
        # BMI calculation
        height = cleaned_data.get('height')
        weight = cleaned_data.get('weight')
        
        if height and weight:
            bmi = weight / ((height / 100) ** 2)
            cleaned_data['bmi'] = bmi
        
        # Blood pressure validation
        systolic = cleaned_data.get('systolic_bp')
        diastolic = cleaned_data.get('diastolic_bp')
        
        if systolic and diastolic:
            if systolic <= diastolic:
                self.add_error('systolic_bp', 'Systolic must be higher than diastolic')
        
        return cleaned_data