"""
Machine Learning Models for Health Risk Prediction

This module provides the core ML functionality for predicting health risks including:
- Heart Disease Risk
- Diabetes Risk
- Cancer Risk
- Stroke Risk

The HealthPredictor class handles model loading, feature engineering, and prediction
generation with comprehensive error handling and logging.

Example:
    >>> from predictor.ml_models import health_predictor
    >>> data = {'systolic_bp': 120, 'diastolic_bp': 80, ...}
    >>> results = health_predictor.predict_health_risks(data)
    >>> print(results['heart_disease_risk'])
"""

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:
    torch = None
    nn = None
    F = None

import numpy as np
try:
    import pandas as pd
except ImportError:
    pd = None

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import logging
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

if torch:
    class HealthRiskNN(nn.Module):
        """Neural Network for Health Risk Prediction"""
        
        def __init__(self, input_size: int, hidden_sizes: List[int] = [128, 64, 32], dropout_rate: float = 0.3):
            super(HealthRiskNN, self).__init__()
            
            self.input_size = input_size
            self.hidden_sizes = hidden_sizes
            self.dropout_rate = dropout_rate
            
            # Input layer
            self.input_layer = nn.Linear(input_size, hidden_sizes[0])
            self.input_bn = nn.BatchNorm1d(hidden_sizes[0])
            self.input_dropout = nn.Dropout(dropout_rate)
            
            # Hidden layers
            self.hidden_layers = nn.ModuleList()
            self.batch_norms = nn.ModuleList()
            self.dropouts = nn.ModuleList()
            
            for i in range(len(hidden_sizes) - 1):
                self.hidden_layers.append(nn.Linear(hidden_sizes[i], hidden_sizes[i + 1]))
                self.batch_norms.append(nn.BatchNorm1d(hidden_sizes[i + 1]))
                self.dropouts.append(nn.Dropout(dropout_rate))
            
            # Output layers for different conditions
            self.heart_disease_output = nn.Linear(hidden_sizes[-1], 1)
            self.diabetes_output = nn.Linear(hidden_sizes[-1], 1)
            self.cancer_output = nn.Linear(hidden_sizes[-1], 1)
            self.stroke_output = nn.Linear(hidden_sizes[-1], 1)
            
            # Initialize weights
            self._initialize_weights()
        
        def _initialize_weights(self):
            """Initialize network weights"""
            for m in self.modules():
                if isinstance(m, nn.Linear):
                    nn.init.xavier_uniform_(m.weight)
                    nn.init.constant_(m.bias, 0)
        
        def forward(self, x):
            """Forward pass through the network"""
            # Input layer
            x = self.input_layer(x)
            x = self.input_bn(x)
            x = F.relu(x)
            x = self.input_dropout(x)
            
            # Hidden layers
            for layer, bn, dropout in zip(self.hidden_layers, self.batch_norms, self.dropouts):
                x = layer(x)
                x = bn(x)
                x = F.relu(x)
                x = dropout(x)
            
            # Output layers
            heart_disease = torch.sigmoid(self.heart_disease_output(x))
            diabetes = torch.sigmoid(self.diabetes_output(x))
            cancer = torch.sigmoid(self.cancer_output(x))
            stroke = torch.sigmoid(self.stroke_output(x))
            
            return {
                'heart_disease': heart_disease,
                'diabetes': diabetes,
                'cancer': cancer,
                'stroke': stroke
            }
else:
    class HealthRiskNN:
        pass

class HealthPredictor:
    """Main class for health prediction using trained models"""
    
    def __init__(self, model_path: str = None):
        self.model_path = Path(model_path) if model_path else Path(__file__).parent.parent / 'ml_models'
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu') if torch else None
        
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.model_version = None
        
        # Feature configuration based on research
        self.numeric_features = [
            'age', 'bmi', 'systolic_bp', 'diastolic_bp', 'heart_rate', 'temperature',
            'total_cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',
            'fasting_glucose', 'hba1c', 'creatinine', 'hemoglobin',
            'stress_level', 'sleep_hours'
        ]
        
        self.categorical_features = [
            'gender', 'smoking_status', 'alcohol_consumption', 'exercise_level', 'family_medical_history'
        ]
        
        self.binary_features = [
            'chest_pain', 'shortness_of_breath', 'fatigue', 'frequent_urination',
            'excessive_thirst', 'unexplained_weight_loss', 'blurred_vision',
            'dizziness', 'palpitations'
        ]
        
        self.load_models()
    
    def load_models(self):
        """Load trained models and scaler"""
        try:
            # Load the main model
            model_file = self.model_path / 'health_risk_model.pth'
            if torch and model_file.exists():
                checkpoint = torch.load(model_file, map_location=self.device)
                self.model = HealthRiskNN(
                    input_size=checkpoint['input_size'],
                    hidden_sizes=checkpoint['hidden_sizes'],
                    dropout_rate=checkpoint.get('dropout_rate', 0.3)
                )
                self.model.load_state_dict(checkpoint['model_state_dict'])
                self.model.to(self.device)
                self.model.eval()
                self.model_version = checkpoint.get('version', '1.0.0')
                logger.info(f"Loaded health risk model version {self.model_version}")
            else:
                logger.warning("No trained model found, using default predictions")
                self.model = None
            
            # Load scaler
            scaler_file = self.model_path / 'feature_scaler.pkl'
            if scaler_file.exists():
                self.scaler = joblib.load(scaler_file)
                logger.info("Loaded feature scaler")
            
            # Load feature names
            features_file = self.model_path / 'feature_names.json'
            if features_file.exists():
                with open(features_file, 'r') as f:
                    self.feature_names = json.load(f)
                logger.info("Loaded feature names")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            self.model = None
            self.scaler = None
    
    def prepare_features(self, assessment_data: Dict) -> np.ndarray:
        """Prepare features for model prediction"""
        features = []
        
        # Numeric features
        for feature in self.numeric_features:
            value = assessment_data.get(feature, 0)
            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    value = 0
            features.append(float(value))
        
        # Categorical features - one-hot encoding
        categorical_mappings = {
            'gender': {'male': 0, 'female': 1, 'other': 2},
            'smoking_status': {'never': 0, 'former': 1, 'current': 2},
            'alcohol_consumption': {'never': 0, 'occasional': 1, 'moderate': 2, 'heavy': 3},
            'exercise_level': {'sedentary': 0, 'light': 1, 'moderate': 2, 'vigorous': 3},
        }
        
        for feature in self.categorical_features:
            if feature == 'family_medical_history':
                # Handle dict-type family medical history
                value = assessment_data.get(feature, {})
                if isinstance(value, dict):
                    # Count number of conditions in family history
                    # 0 = none, 1-2 = single condition, 3+ = multiple
                    num_conditions = sum(1 for v in value.values() if v)
                    if num_conditions == 0:
                        encoded_value = 0  # none
                    elif num_conditions == 1:
                        # Single condition - map to specific value
                        if value.get('heart_disease'):
                            encoded_value = 1
                        elif value.get('diabetes'):
                            encoded_value = 2
                        elif value.get('cancer'):
                            encoded_value = 3
                        else:
                            encoded_value = 1  # default to heart disease
                    else:
                        encoded_value = 4  # multiple conditions
                elif isinstance(value, str):
                    # Handle string values for backward compatibility
                    mapping = {'none': 0, 'heart_disease': 1, 'diabetes': 2, 'cancer': 3, 'multiple': 4}
                    encoded_value = mapping.get(value, 0)
                else:
                    encoded_value = 0
                features.append(encoded_value)
            else:
                value = assessment_data.get(feature, 'none')
                mapping = categorical_mappings.get(feature, {})
                encoded_value = mapping.get(value, 0)
                features.append(encoded_value)
        
        # Binary features
        for feature in self.binary_features:
            value = assessment_data.get(feature, False)
            features.append(1 if value else 0)
        
        return np.array(features).reshape(1, -1)
    
    def predict_health_risks(self, assessment_data: Dict) -> Dict:
        """Predict health risks using the trained model"""
        start_time = torch.cuda.Event(enable_timing=True) if torch and torch.cuda.is_available() else None
        end_time = torch.cuda.Event(enable_timing=True) if torch and torch.cuda.is_available() else None
        
        if start_time:
            start_time.record()
        
        try:
            # Prepare features
            features = self.prepare_features(assessment_data)
            
            # Scale features if scaler is available
            if self.scaler:
                features = self.scaler.transform(features)
            
            # Convert to tensor
            if torch:
                features_tensor = torch.FloatTensor(features).to(self.device)
            else:
                features_tensor = None
            
            # Make predictions
            if self.model:
                with torch.no_grad():
                    predictions = self.model(features_tensor)
                
                # Convert predictions to risk scores (0-100)
                results = {
                    'heart_disease_risk': float(predictions['heart_disease'].item()) * 100,
                    'diabetes_risk': float(predictions['diabetes'].item()) * 100,
                    'cancer_risk': float(predictions['cancer'].item()) * 100,
                    'stroke_risk': float(predictions['stroke'].item()) * 100,
                    'prediction_confidence': 0.85  # Default confidence
                }
            else:
                # Fallback to rule-based predictions if model not available
                results = self._rule_based_prediction(assessment_data)
            
            # Calculate prediction time
            if start_time:
                end_time.record()
                if torch:
                    torch.cuda.synchronize()
                prediction_time_ms = start_time.elapsed_time(end_time)
            else:
                import time
                prediction_time_ms = time.time() * 1000  # Placeholder
            
            results['prediction_time_ms'] = prediction_time_ms
            results['model_version'] = self.model_version or 'rule-based'
            
            # Add risk categories
            results.update(self._categorize_risks(results))
            
            # Generate recommendations
            results['recommendations'] = self._generate_recommendations(results, assessment_data)
            
            # Calculate feature importance (simplified)
            results['feature_importance'] = self._calculate_feature_importance(assessment_data)
            
            return results
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return self._error_prediction()
    
    def _rule_based_prediction(self, data: Dict) -> Dict:
        """Fallback rule-based prediction when ML model is not available"""
        
        # Heart disease risk calculation
        heart_risk = 0
        if data.get('age', 0) > 65:
            heart_risk += 15
        elif data.get('age', 0) > 45:
            heart_risk += 8
        
        if data.get('systolic_bp', 0) > 140 or data.get('diastolic_bp', 0) > 90:
            heart_risk += 20
        elif data.get('systolic_bp', 0) > 130 or data.get('diastolic_bp', 0) > 80:
            heart_risk += 10
        
        if data.get('total_cholesterol', 0) > 240:
            heart_risk += 15
        elif data.get('total_cholesterol', 0) > 200:
            heart_risk += 8
        
        if data.get('smoking_status') == 'current':
            heart_risk += 25
        elif data.get('smoking_status') == 'former':
            heart_risk += 10
        
        if data.get('chest_pain') or data.get('shortness_of_breath'):
            heart_risk += 20
        
        # Diabetes risk calculation
        diabetes_risk = 0
        if data.get('fasting_glucose', 0) > 126:
            diabetes_risk += 30
        elif data.get('fasting_glucose', 0) > 100:
            diabetes_risk += 15
        
        if data.get('hba1c', 0) > 6.5:
            diabetes_risk += 25
        elif data.get('hba1c', 0) > 5.7:
            diabetes_risk += 12
        
        if data.get('bmi', 0) > 30:
            diabetes_risk += 20
        elif data.get('bmi', 0) > 25:
            diabetes_risk += 10
        
        if data.get('frequent_urination') or data.get('excessive_thirst'):
            diabetes_risk += 15
        
        # Cancer risk calculation
        cancer_risk = 0
        if data.get('age', 0) > 60:
            cancer_risk += 15
        elif data.get('age', 0) > 40:
            cancer_risk += 8
        
        if data.get('smoking_status') == 'current':
            cancer_risk += 35
        elif data.get('smoking_status') == 'former':
            cancer_risk += 15
        
        if data.get('family_medical_history') in ['cancer', 'multiple']:
            cancer_risk += 20
        
        # Stroke risk calculation
        stroke_risk = max(heart_risk * 0.7, diabetes_risk * 0.6)
        
        return {
            'heart_disease_risk': min(100, heart_risk),
            'diabetes_risk': min(100, diabetes_risk),
            'cancer_risk': min(100, cancer_risk),
            'stroke_risk': min(100, stroke_risk),
            'prediction_confidence': 0.75,
            'prediction_method': 'rule-based'
        }
    
    def _categorize_risks(self, risks: Dict) -> Dict:
        """Categorize risk levels"""
        def get_category(risk_score):
            if risk_score < 20:
                return 'low'
            elif risk_score < 50:
                return 'moderate'
            elif risk_score < 75:
                return 'high'
            else:
                return 'very_high'
        
        return {
            'heart_disease_category': get_category(risks['heart_disease_risk']),
            'diabetes_category': get_category(risks['diabetes_risk']),
            'cancer_category': get_category(risks['cancer_risk']),
            'stroke_category': get_category(risks['stroke_risk'])
        }
    
    def _generate_recommendations(self, risks: Dict, data: Dict) -> List[Dict]:
        """Generate personalized health recommendations"""
        recommendations = []
        
        # Heart disease recommendations
        if risks['heart_disease_risk'] >= 50:
            recommendations.append({
                'category': 'Cardiovascular',
                'priority': 'high' if risks['heart_disease_risk'] >= 75 else 'medium',
                'title': 'Cardiovascular Health Assessment',
                'description': 'Consider consulting a cardiologist for comprehensive heart health evaluation.',
                'actions': ['Schedule cardiology consultation', 'Monitor blood pressure regularly', 'Consider stress testing']
            })
        
        # Diabetes recommendations
        if risks['diabetes_risk'] >= 50:
            recommendations.append({
                'category': 'Endocrine',
                'priority': 'high' if risks['diabetes_risk'] >= 75 else 'medium',
                'title': 'Diabetes Risk Management',
                'description': 'Lifestyle modifications and glucose monitoring are recommended.',
                'actions': ['Consult endocrinologist', 'Implement diabetic diet', 'Monitor blood glucose levels']
            })
        
        # General health recommendations
        if data.get('bmi', 0) > 25:
            recommendations.append({
                'category': 'Lifestyle',
                'priority': 'medium',
                'title': 'Weight Management',
                'description': 'Achieving a healthy weight can reduce multiple health risks.',
                'actions': ['Consult nutritionist', 'Increase physical activity', 'Monitor caloric intake']
            })
        
        if data.get('smoking_status') in ['current', 'former']:
            recommendations.append({
                'category': 'Lifestyle',
                'priority': 'high',
                'title': 'Smoking Cessation',
                'description': 'Quitting smoking significantly reduces cardiovascular and cancer risks.',
                'actions': ['Join smoking cessation program', 'Consider nicotine replacement therapy', 'Seek behavioral support']
            })
        
        return recommendations
    
    def _calculate_feature_importance(self, data: Dict) -> Dict:
        """Calculate simplified feature importance"""
        importance = {}
        
        # Age importance
        age = data.get('age', 0)
        importance['age'] = min(age / 100, 1.0) * 100
        
        # Blood pressure importance
        systolic_bp = data.get('systolic_bp', 0)
        importance['blood_pressure'] = min(systolic_bp / 180, 1.0) * 100
        
        # BMI importance
        bmi = data.get('bmi', 0)
        if bmi > 25:
            importance['bmi'] = min((bmi - 25) / 15, 1.0) * 100
        else:
            importance['bmi'] = 0
        
        # Glucose importance
        glucose = data.get('fasting_glucose', 0)
        if glucose > 100:
            importance['glucose'] = min((glucose - 100) / 200, 1.0) * 100
        else:
            importance['glucose'] = 0
        
        return importance
    
    def _error_prediction(self) -> Dict:
        """Return error prediction with safe defaults"""
        return {
            'heart_disease_risk': 25.0,
            'diabetes_risk': 25.0,
            'cancer_risk': 25.0,
            'stroke_risk': 25.0,
            'heart_disease_category': 'moderate',
            'diabetes_category': 'moderate',
            'cancer_category': 'moderate',
            'stroke_category': 'moderate',
            'prediction_confidence': 0.5,
            'prediction_method': 'error-fallback',
            'model_version': 'error-fallback',
            'prediction_time_ms': 0,
            'recommendations': [],
            'feature_importance': {},
            'error': True
        }

# Global predictor instance
health_predictor = HealthPredictor()