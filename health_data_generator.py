import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

class HealthDataGenerator:
    def __init__(self):
        self.risk_factors = {
            'age': {'mean': 52, 'std': 15, 'range': (18, 90)},
            'bmi': {'mean': 27.5, 'std': 5.5, 'range': (15, 50)},
            'systolic_bp': {'mean': 130, 'std': 20, 'range': (90, 200)},
            'diastolic_bp': {'mean': 82, 'std': 12, 'range': (60, 120)},
            'cholesterol': {'mean': 210, 'std': 45, 'range': (120, 400)},
            'glucose': {'mean': 105, 'std': 35, 'range': (70, 300)},
            'hbalc': {'mean': 5.8, 'std': 1.2, 'range': (4.0, 12.0)},
            'creatinine': {'mean': 1.0, 'std': 0.3, 'range': (0.5, 3.0)},
            'hemoglobin': {'mean': 14.2, 'std': 1.8, 'range': (9.0, 18.0)}
        }
        
        self.lifestyle_factors = {
            'smoking': ['never', 'former', 'current'],
            'alcohol': ['never', 'occasional', 'moderate', 'heavy'],
            'exercise': ['sedentary', 'light', 'moderate', 'vigorous'],
            'diet': ['poor', 'fair', 'good', 'excellent'],
            'stress': ['low', 'moderate', 'high', 'severe']
        }
        
        self.medical_history = {
            'family_history': ['none', 'heart_disease', 'diabetes', 'cancer', 'multiple'],
            'previous_conditions': ['none', 'hypertension', 'diabetes', 'heart_disease', 'stroke'],
            'medications': ['none', 'bp_meds', 'diabetes_meds', 'statins', 'multiple']
        }

    def generate_patient_data(self, n_samples=10000):
        """Generate comprehensive patient health data"""
        data = []
        
        for i in range(n_samples):
            # Basic demographics
            age = max(18, min(90, int(np.random.normal(self.risk_factors['age']['mean'], 
                                                      self.risk_factors['age']['std']))))
            gender = np.random.choice(['male', 'female'], p=[0.48, 0.52])
            
            # Physical measurements
            bmi = max(15, min(50, np.random.normal(self.risk_factors['bmi']['mean'], 
                                                  self.risk_factors['bmi']['std'])))
            systolic_bp = max(90, min(200, int(np.random.normal(self.risk_factors['systolic_bp']['mean'], 
                                                              self.risk_factors['systolic_bp']['std']))))
            diastolic_bp = max(60, min(120, int(np.random.normal(self.risk_factors['diastolic_bp']['mean'], 
                                                               self.risk_factors['diastolic_bp']['std']))))
            
            # Lab results
            cholesterol = max(120, min(400, int(np.random.normal(self.risk_factors['cholesterol']['mean'], 
                                                                self.risk_factors['cholesterol']['std']))))
            glucose = max(70, min(300, int(np.random.normal(self.risk_factors['glucose']['mean'], 
                                                           self.risk_factors['glucose']['std']))))
            hbalc = max(4.0, min(12.0, np.random.normal(self.risk_factors['hbalc']['mean'], 
                                                      self.risk_factors['hbalc']['std'])))
            creatinine = max(0.5, min(3.0, np.random.normal(self.risk_factors['creatinine']['mean'], 
                                                           self.risk_factors['creatinine']['std'])))
            hemoglobin = max(9.0, min(18.0, np.random.normal(self.risk_factors['hemoglobin']['mean'], 
                                                            self.risk_factors['hemoglobin']['std'])))
            
            # Lifestyle factors
            smoking = np.random.choice(self.lifestyle_factors['smoking'], p=[0.55, 0.25, 0.20])
            alcohol = np.random.choice(self.lifestyle_factors['alcohol'], p=[0.30, 0.35, 0.25, 0.10])
            exercise = np.random.choice(self.lifestyle_factors['exercise'], p=[0.40, 0.30, 0.20, 0.10])
            diet = np.random.choice(self.lifestyle_factors['diet'], p=[0.20, 0.35, 0.30, 0.15])
            stress = np.random.choice(self.lifestyle_factors['stress'], p=[0.25, 0.40, 0.25, 0.10])
            
            # Medical history
            family_history = np.random.choice(self.medical_history['family_history'], 
                                            p=[0.40, 0.20, 0.15, 0.15, 0.10])
            previous_conditions = np.random.choice(self.medical_history['previous_conditions'], 
                                                  p=[0.60, 0.20, 0.10, 0.05, 0.05])
            medications = np.random.choice(self.medical_history['medications'], 
                                         p=[0.50, 0.20, 0.10, 0.10, 0.10])
            
            # Calculate risk scores based on research findings
            heart_risk = self.calculate_heart_risk(age, gender, bmi, systolic_bp, diastolic_bp, 
                                                  cholesterol, glucose, smoking, family_history)
            diabetes_risk = self.calculate_diabetes_risk(age, bmi, glucose, hbalc, family_history, 
                                                        previous_conditions)
            cancer_risk = self.calculate_cancer_risk(age, gender, smoking, family_history, 
                                                   previous_conditions, diet)
            
            # Generate symptoms based on risk levels
            symptoms = self.generate_symptoms(heart_risk, diabetes_risk, cancer_risk)
            
            patient_data = {
                'patient_id': f'P{str(i+1).zfill(6)}',
                'age': age,
                'gender': gender,
                'bmi': round(bmi, 1),
                'systolic_bp': systolic_bp,
                'diastolic_bp': diastolic_bp,
                'cholesterol': cholesterol,
                'glucose': glucose,
                'hbalc': round(hbalc, 1),
                'creatinine': round(creatinine, 2),
                'hemoglobin': round(hemoglobin, 1),
                'smoking': smoking,
                'alcohol': alcohol,
                'exercise': exercise,
                'diet': diet,
                'stress': stress,
                'family_history': family_history,
                'previous_conditions': previous_conditions,
                'medications': medications,
                'heart_disease_risk': heart_risk,
                'diabetes_risk': diabetes_risk,
                'cancer_risk': cancer_risk,
                'symptoms': symptoms,
                'assessment_date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
            }
            
            data.append(patient_data)
        
        return pd.DataFrame(data)

    def calculate_heart_risk(self, age, gender, bmi, systolic_bp, diastolic_bp, 
                           cholesterol, glucose, smoking, family_history):
        """Calculate heart disease risk score (0-100)"""
        risk_score = 0
        
        # Age factor
        if age >= 75:
            risk_score += 15
        elif age >= 65:
            risk_score += 12
        elif age >= 55:
            risk_score += 8
        elif age >= 45:
            risk_score += 5
        
        # Gender factor
        if gender == 'male':
            risk_score += 3
        
        # BMI factor
        if bmi >= 30:
            risk_score += 8
        elif bmi >= 25:
            risk_score += 4
        
        # Blood pressure factor
        if systolic_bp >= 140 or diastolic_bp >= 90:
            risk_score += 10
        elif systolic_bp >= 130 or diastolic_bp >= 80:
            risk_score += 5
        
        # Cholesterol factor
        if cholesterol >= 240:
            risk_score += 8
        elif cholesterol >= 200:
            risk_score += 4
        
        # Glucose factor
        if glucose >= 126:
            risk_score += 8
        elif glucose >= 100:
            risk_score += 3
        
        # Smoking factor
        if smoking == 'current':
            risk_score += 12
        elif smoking == 'former':
            risk_score += 5
        
        # Family history factor
        if family_history in ['heart_disease', 'multiple']:
            risk_score += 8
        
        return min(100, risk_score)

    def calculate_diabetes_risk(self, age, bmi, glucose, hbalc, family_history, previous_conditions):
        """Calculate diabetes risk score (0-100)"""
        risk_score = 0
        
        # Age factor
        if age >= 65:
            risk_score += 12
        elif age >= 45:
            risk_score += 8
        elif age >= 35:
            risk_score += 4
        
        # BMI factor
        if bmi >= 35:
            risk_score += 15
        elif bmi >= 30:
            risk_score += 10
        elif bmi >= 25:
            risk_score += 5
        
        # Glucose factor
        if glucose >= 126:
            risk_score += 20
        elif glucose >= 100:
            risk_score += 10
        
        # HbA1c factor
        if hbalc >= 6.5:
            risk_score += 15
        elif hbalc >= 5.7:
            risk_score += 8
        
        # Family history factor
        if family_history in ['diabetes', 'multiple']:
            risk_score += 10
        
        # Previous conditions factor
        if previous_conditions == 'diabetes':
            risk_score += 25
        
        return min(100, risk_score)

    def calculate_cancer_risk(self, age, gender, smoking, family_history, previous_conditions, diet):
        """Calculate cancer risk score (0-100)"""
        risk_score = 0
        
        # Age factor
        if age >= 70:
            risk_score += 15
        elif age >= 60:
            risk_score += 10
        elif age >= 50:
            risk_score += 6
        elif age >= 40:
            risk_score += 3
        
        # Smoking factor
        if smoking == 'current':
            risk_score += 20
        elif smoking == 'former':
            risk_score += 8
        
        # Family history factor
        if family_history in ['cancer', 'multiple']:
            risk_score += 12
        
        # Diet factor
        if diet == 'poor':
            risk_score += 8
        elif diet == 'fair':
            risk_score += 4
        
        # Previous conditions factor
        if previous_conditions in ['diabetes', 'heart_disease']:
            risk_score += 5
        
        return min(100, risk_score)

    def generate_symptoms(self, heart_risk, diabetes_risk, cancer_risk):
        """Generate symptoms based on risk levels"""
        symptoms = []
        
        # Heart disease symptoms
        if heart_risk >= 70:
            symptoms.extend(['chest_pain', 'shortness_of_breath', 'fatigue', 'irregular_heartbeat'])
        elif heart_risk >= 50:
            symptoms.extend(['mild_chest_discomfort', 'occasional_shortness_of_breath', 'fatigue'])
        elif heart_risk >= 30:
            symptoms.extend(['occasional_fatigue', 'mild_shortness_of_breath'])
        
        # Diabetes symptoms
        if diabetes_risk >= 70:
            symptoms.extend(['frequent_urination', 'excessive_thirst', 'unexplained_weight_loss', 'blurred_vision'])
        elif diabetes_risk >= 50:
            symptoms.extend(['increased_thirst', 'frequent_urination', 'mild_fatigue'])
        elif diabetes_risk >= 30:
            symptoms.extend(['mild_thirst', 'occasional_fatigue'])
        
        # General symptoms based on overall health
        if max(heart_risk, diabetes_risk, cancer_risk) >= 60:
            symptoms.append('general_fatigue')
        
        # Remove duplicates and limit to max 5 symptoms
        symptoms = list(set(symptoms))[:5]
        
        return symptoms if symptoms else ['no_significant_symptoms']

    def save_datasets(self):
        """Generate and save all datasets"""
        print("Generating comprehensive health dataset...")
        df = self.generate_patient_data(10000)
        
        # Save main dataset
        df.to_csv('/mnt/okcomputer/output/health_prediction_data.csv', index=False)
        print(f"Saved main dataset: {len(df)} records")
        
        # Create training subset
        train_df = df.sample(n=8000, random_state=42)
        train_df.to_csv('/mnt/okcomputer/output/training_data.csv', index=False)
        print(f"Saved training dataset: {len(train_df)} records")
        
        # Create test subset
        test_df = df.drop(train_df.index)
        test_df.to_csv('/mnt/okcomputer/output/test_data.csv', index=False)
        print(f"Saved test dataset: {len(test_df)} records")
        
        # Create high-risk subset for demonstration
        high_risk_df = df[
            (df['heart_disease_risk'] >= 70) | 
            (df['diabetes_risk'] >= 70) | 
            (df['cancer_risk'] >= 70)
        ].copy()
        high_risk_df.to_csv('/mnt/okcomputer/output/high_risk_patients.csv', index=False)
        print(f"Saved high-risk dataset: {len(high_risk_df)} records")
        
        # Generate summary statistics
        summary = {
            'total_patients': len(df),
            'age_range': f"{df['age'].min()}-{df['age'].max()}",
            'gender_distribution': df['gender'].value_counts().to_dict(),
            'risk_distributions': {
                'heart_disease': {
                    'low_risk (<30)': len(df[df['heart_disease_risk'] < 30]),
                    'moderate_risk (30-50)': len(df[(df['heart_disease_risk'] >= 30) & (df['heart_disease_risk'] < 50)]),
                    'high_risk (50-70)': len(df[(df['heart_disease_risk'] >= 50) & (df['heart_disease_risk'] < 70)]),
                    'very_high_risk (>=70)': len(df[df['heart_disease_risk'] >= 70])
                },
                'diabetes': {
                    'low_risk (<30)': len(df[df['diabetes_risk'] < 30]),
                    'moderate_risk (30-50)': len(df[(df['diabetes_risk'] >= 30) & (df['diabetes_risk'] < 50)]),
                    'high_risk (50-70)': len(df[(df['diabetes_risk'] >= 50) & (df['diabetes_risk'] < 70)]),
                    'very_high_risk (>=70)': len(df[df['diabetes_risk'] >= 70])
                },
                'cancer': {
                    'low_risk (<30)': len(df[df['cancer_risk'] < 30]),
                    'moderate_risk (30-50)': len(df[(df['cancer_risk'] >= 30) & (df['cancer_risk'] < 50)]),
                    'high_risk (50-70)': len(df[(df['cancer_risk'] >= 50) & (df['cancer_risk'] < 70)]),
                    'very_high_risk (>=70)': len(df[df['cancer_risk'] >= 70])
                }
            }
        }
        
        with open('/mnt/okcomputer/output/dataset_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("Dataset generation completed!")
        print(f"Files saved to /mnt/okcomputer/output/")
        return df, summary

if __name__ == "__main__":
    generator = HealthDataGenerator()
    df, summary = generator.save_datasets()